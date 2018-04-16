#!/usr/bin/env python
from PyDEx import *
from MIC4Config import MIC4Config
import socket
import time
import numpy as nm

isDebug = True

class WaveFormGetter:
    def __init__(self):
        self.hostname = "192.168.2.4"                #wire network hostname
        self.port = 5025                             #host tcp port
        self.ss = None
        self.saveDataToFile = None

    def connect(self):
        self.ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
        self.ss.connect((self.hostname,self.port))                                 #connect to the server
        self.ss.send("*IDN?;")                           #read back device ID
        print "Connected to Instrument with ID: %s"%self.ss.recv(128)   

    def getData(self):
        ss = self.ss
        ss.send(":TIMebase:POSition?;")             #Query X-axis timebase position 
        Timebase_Poistion = float(ss.recv(128)[1:])
        print "Timebase_Position:%.6f"%Timebase_Poistion

        ss.send(":WAVeform:XRANge?;")               #Query X-axis range 
        X_Range = float(ss.recv(128)[1:])
        print "XRange:%g"%X_Range


        ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
        Y_Range = float(ss.recv(128)[1:])   
        print "YRange:%f"%Y_Range
        #Y_Factor = Y_Range/980.0
        Y_Factor = Y_Range/62712.0
        #print Y_Factor

        ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        Sample_point = int(ss.recv(128)[1:])  
        print "Sample Point:%d"%Sample_point
 
        ss.send(":CHANnel1:OFFset?;")               #Channel1 Offset 
        CH1_Offset = float(ss.recv(128)[1:])   
        print "Channel 1 Offset:%f"%CH1_Offset
        print "X_Range:%g"%X_Range 
        if X_Range >= 2.0:
            Xrange = nm.arange(-X_Range/2.0,X_Range/2.0,X_Range*1.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion
        elif X_Range < 2.0 and X_Range >= 0.002:
            Xrange = nm.arange((-X_Range*1000)/2.0,(X_Range*1000)/2.0,X_Range*1000.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion * 1000.0
        elif X_Range < 0.002 and X_Range >= 0.000002:
            Xrange = nm.arange((-X_Range*1000000)/2.0,(X_Range*1000000)/2.0,X_Range*1000000.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion * 1000000.0
        else:
            Xrange = nm.arange((-X_Range*1000000000)/2.0,(X_Range*1000000000)/2.0,X_Range*1000000000.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion * 1000000000.0


        ss.send(":ACQuire:SRATe:ANALog?;")          #Query sample rate
        Sample_Rate = float(ss.recv(128)[1:])   
        print "Sample rate:%g"%Sample_Rate
        total_point = Sample_Rate * X_Range
        print total_point


        ss.send(":CHANnel1:OFFset?;")               #Channel1 Offset 
        CH1_Offset = float(ss.recv(128)[1:])   

        ss.send(":SYSTem:HEADer OFF;")              #Query analog store depth
        ss.send(":WAVeform:SOURce CHANnel1;")       #Waveform source 
        ss.send(":WAVeform:BYTeorder LSBFirst;")    #Waveform data byte order
        ss.send(":WAVeform:FORMat WORD;")           #Waveform data format
        ss.send(":WAVeform:STReaming 1;")           #Waveform streaming on
        ss.send(":WAVeform:DATA? 1,%d;"%int(total_point))         #Query waveform data with start address and length

        ### Why these magic numbers 2 and 3? A number contains 2 words? And there is a header with 3 words?
        n = total_point * 2 + 3
        totalContent = ""
        totalRecved = 0
        while totalRecved < n:                      #fetch data
            #print n, (n-totalRecved)
            onceContent = ss.recv(int(n - totalRecved))
            #print len(onceContent)
            totalContent += onceContent
            totalRecved = len(totalContent)
        length = len(totalContent[3:])              #print length
        sample = [0]*(length/2)
        print length/2
        for i in xrange(length/2):              #store data into file
            ### combine two words to form the number
            digital_number = (ord(totalContent[3+i*2+1])<<8)+ord(totalContent[3+i*2])
            if (ord(totalContent[3+i*2+1]) & 0x80) == 0x80:             
                sample[i] = (digital_number - 65535+1000)*Y_Factor + CH1_Offset
            else:
                sample[i] = (digital_number+1000)*Y_Factor + CH1_Offset
            if self.saveDataToFile:
#                 self.saveDataToFile.write(str(i)+' '+str(sample[i])+" %f".format(Xrange[i] + Timebase_Poistion_X)+'\n')
                self.saveDataToFile.write(str(i)+' '+str(sample[i])+'\n')
        return sample



    def showSample(self,sample):
        '''Check the sample, for debug'''
        pass


class dataTaker:
    def __init__(self,outFileName=None):
        self.mic4 = MIC4Config()
        self.wave = WaveFormGetter()
        self.outFileName = outFileName

    def connect(self):
        self.mic4.connect()
        self.wave.connect()
    
    def analysis(self, sample):
        '''Use the first half for background study and the second half for signal extraction'''
        Nhalf = len(sample)/2
        ## The the average and RMS of the first half
        mean1 = nm.mean(sample[:Nhalf-50])
        
        ## Get the second half after subtracting the background
        sample2 = [x-mean1 for x in sample[Nhalf+600:]]

        ## get the avarage maximum of the second half, calculate the amplitude
        maxI2, max2 = max(enumerate(sample2), key=lambda p:p[1])
        mean2 = nm.mean(sample2[max(maxI2-150,0):maxI2+150])
        if isDebug: print mean1,mean2,maxI2, max2

        return mean2

class DeltaUScanner(dataTaker):
    def __init__(self,outFileName=None):
        dataTaker.__init__(self,outFileName)

    def setup(self):
        self.connect()
        self.mic4.sReg.setPar('VCLIP' ,0  , 0.689, 0x200)
        self.mic4.sReg.setPar('VReset',1.1, 0.703, 0x200)
        self.mic4.sReg.setPar('VCASN2',0.5, 0.693, 0x200)
        self.mic4.sReg.setPar('VCASN' ,0.4, 0.689, 0x200)
        self.mic4.sReg.setPar('VCASP' ,0.6, 0.694, 0x200)
        self.mic4.sReg.setPar('VRef'  ,0.4, 0.701, 0x200)
        self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
        self.mic4.sReg.setPar('IDB'   ,0xf0)
        self.mic4.sReg.setPar('ITHR'  ,0x80)
        self.mic4.sReg.setPar('IRESET',0x80)
        self.mic4.sReg.setPar('IDB2'  ,0x80)
        self.mic4.sReg.selectVolDAC(0)
        self.mic4.sReg.selectCurDAC(5)
        self.mic4.sReg.selectCol(11)

        self.mic4.sReg.show()
        self.mic4.testReg(read=True)

    def measure(self, vH, vL, N=1):
        cmdStr = ''
        cmdStr += self.mic4.dac.turn_on_2V5_ref()			#turn on internal reference voltage
        cmdStr += self.mic4.dac.set_voltage(0, 1.2) # LT_VREF
        cmdStr += self.mic4.dac.set_voltage(2, vH) # VPLUSE_HIGH
        cmdStr += self.mic4.dac.set_voltage(3, 1.2) # LVDS_REF
        cmdStr += self.mic4.dac.set_voltage(4, vL) # VPULSE_LOW
        cmdStr += self.mic4.dac.set_voltage(6, 1.2) # DAC_REF
        self.mic4.s.sendall(cmdStr)

        ### average of 10 measurements
        vals = []
        for k in range(N):
            time.sleep(1)
            self.mic4.sendA_PULSE()
            time.sleep(1)
            sample = self.wave.getData()
            v = self.analysis(sample)
            vals.append(v)
        mean = nm.mean(vals)
        err  = nm.std(vals)
        print vals
        print vL, vH, mean, err
        return mean, err

    def run(self):
        N = 10

        fout = open(self.outFileName,'w') if self.outFileName else None
        ### loop over
        for i in range(16):
            iV = 0.1*i
            for j in range(i,16):
                jV = 0.1*j
                ### Then setup DAC8568
                mean,err = self.measure(jV, iV, N)    
                if fout:
                    fout.write('{0:.2f} {1:.2f} {2:.4f} {3:.4f}\n'.format(iV, jV, mean, err))

def test_DeltaUScanner():
    t1 = DeltaUScanner("test1_out.dat")
    t1.setup()
    t1.measure(1.5,0.4)
#     t1.run()


class Tuner(dataTaker):
    def __init__(self,outFileName=None):
        dataTaker.__init__(self,outFileName)

        self.Col = 0
        self.VolDAC = 0
        self.CurDAC = 0
        self.atBounds = None
        self.atMaxIters = 100
        self.fout = None
        self.N = 10

    def setup(self):
        self.connect()
        self.mic4.test_DAC8568_config()
        if self.outFileName: self.fout = open(self.outFileName,'w')

    def tune(self):
        de = DE(self.auto_tune_fun, self.atBounds, maxiters=self.atMaxIters)
        ret = de.solve()
        print(ret)

    def auto_tune_fun(self,x):
        '''The function that takes the parameters and return the score'''
        ### send the 200 bit reg to setup DAC -- DAC8568 should already have been set
        self.mic4.sReg.value =  0
        self.mic4.sReg.setPDB(0)
        ## chip-5
        self.mic4.sReg.setPar('VCLIP'   ,x[0],0.689, 0x200)
        self.mic4.sReg.setPar('VReset'  ,x[1],0.703, 0x200)
        self.mic4.sReg.setPar('VCASN2'  ,x[2],0.693, 0x200)
        self.mic4.sReg.setPar('VCASN'   ,x[3],0.689, 0x200)
        self.mic4.sReg.setPar('VCASP'   ,x[4],0.694, 0x200)
        self.mic4.sReg.setPar('VRef'    ,0.4 ,0.701, 0x200)
        self.mic4.sReg.setPar('IBIAS'   ,int(x[5]))
        self.mic4.sReg.setPar('IDB'     ,int(x[6]))
        self.mic4.sReg.setPar('ITHR'    ,int(x[7]))
        self.mic4.sReg.setPar('IRESET'  ,0x80)
        self.mic4.sReg.setPar('IDB2'    ,0x80)
        self.mic4.sReg.selectVolDAC(self.VolDAC)
        self.mic4.sReg.selectCurDAC(self.CurDAC)
        self.mic4.sReg.selectCol(self.Col)

        self.mic4.sReg.show()
        self.mic4.testReg(read=True)

        ### average of 10 measurements
        vals = []
        for k in range(self.N):
            time.sleep(1)
            self.mic4.sendA_PULSE()
            time.sleep(1)
            sample = self.wave.getData()
            v = self.analysis(sample)
            vals.append(v)
        mean = nm.mean(vals)
        err  = nm.std(vals)
        if isDebug:
            print vals
            print x, mean, err
        if self.fout:
            vs = [str(a) for a in vals]
            print vs
            self.fout.write('#Val:'+','.join([str(a) for a in vals])+'\n')
            self.fout.write(' '.join([str(a) for a in x])+' '+str(mean)+' '+str(err)+'\n')

        print "return value:", -mean
        return -mean

    def analysis2(self, sample):
        '''Use the first half for background study and the second half for signal extraction'''
        Nhalf = len(sample)/2
        ## The the average and RMS of the first half
        mean1 = nm.mean(sample[:Nhalf-50])
        
        ## Get the second half after subtracting the background
        sample2 = [x-mean1 for x in sample[Nhalf+600:]]

        ## get the avarage maximum of the second half, calculate the amplitude
        maxI2, max2 = max(enumerate(sample2), key=lambda p:p[1])
        mean2 = nm.mean(sample2[max(maxI2-150,0):maxI2+150])
        if isDebug: print mean1,mean2,maxI2, max2

        return -mean2

    def setUpTest(self):
        self.atBounds = [(-10,10)]

def runTune():
    t1 = Tuner("tune_out2.dat")
    t1.setup()
#     t1.auto_tune_fun([0,1.1,0.5,0.4,0.6, 0xff, 0xf0, 0x80])
#     t1.setUpTest()
    t1.atBounds = [(0,0.5),(0.5,1.49),(0.2,1.4),(0.3,1.0),(0.2,1.4),(0,0xff),(0,0xff),(0,0xff)]
    t1.tune()

if __name__ == '__main__':
    runTune()
#     test_DeltaUScanner()
