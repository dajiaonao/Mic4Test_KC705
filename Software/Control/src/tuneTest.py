#!/usr/bin/env python
from PyDEx import *
from MIC4Config import MIC4Config
import socket
import time
import numpy as nm
from sampleTest import sampler
import math

isDebug = True

class WaveFormGetter:
    def __init__(self):
        self.hostname = "192.168.2.4"                #wire network hostname
        self.port = 5025                             #host tcp port
        self.ss = None
        self.saveDataToFile = None
        self.channel = 2

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


        ss.send(":WAVeform:SOURce CHANnel{0:d};".format(self.channel))       #Waveform source 
        ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
        Y_Range = float(ss.recv(128)[1:])   
        print "YRange:%f"%Y_Range
        #Y_Factor = Y_Range/980.0
        Y_Factor = Y_Range/62712.0
        #print Y_Factor

        ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        Sample_point = int(ss.recv(128)[1:])  
        print "Sample Point:%d"%Sample_point
 
        ss.send(":CHANnel{0:d}:OFFset?;".format(self.channel))               #Channel1 Offset 
        CH1_Offset = float(ss.recv(128)[1:])   
        print "Channel %d Offset:%f"%(self.channel, CH1_Offset)
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
        total_point = int(Sample_Rate * X_Range)
        print total_point


        ss.send(":CHANnel{0:d}:OFFset?;".format(self.channel))               #Channel1 Offset 
        CH1_Offset = float(ss.recv(128)[1:])   

        ss.send(":SYSTem:HEADer OFF;")              #Query analog store depth
        ss.send(":WAVeform:BYTeorder LSBFirst;")    #Waveform data byte order
        ss.send(":WAVeform:FORMat WORD;")           #Waveform data format
        ss.send(":WAVeform:STReaming 1;")           #Waveform streaming on
        ss.send(":WAVeform:DATA? 1,%d;"%total_point)         #Query waveform data with start address and length

        ### Why these magic numbers 2 and 3? A number contains 2 words? And there is a header with 3 words?
        n = total_point * 2 + 3
        totalContent = ""
        totalRecved = 0
        while totalRecved < n:                      #fetch data
            onceContent = ss.recv(n - totalRecved)
#             print len(onceContent),totalRecved,
            totalContent += onceContent
            totalRecved = len(totalContent)
#             print totalRecved
        length = len(totalContent[3:])/2              #print length
        sample = [0]*length
        print length
        for i in range(length):              #store data into file
            ### combine two words to form the number
            digital_number = (ord(totalContent[3+i*2+1])<<8)+ord(totalContent[3+i*2])
            if (ord(totalContent[3+i*2+1]) & 0x80) == 0x80:             
                sample[i] = (digital_number - 65535+1000)*Y_Factor + CH1_Offset
            else:
                sample[i] = (digital_number+1000)*Y_Factor + CH1_Offset
            if self.saveDataToFile:
#                 self.saveDataToFile.write(str(i)+' '+str(sample[i])+" %f".format(Xrange[i] + Timebase_Poistion_X)+'\n')
                self.saveDataToFile.write(str(i)+' '+str(sample[i])+'\n')
#                 print 'saving data'
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
    
    def analysis(self, sample, nB=50, nS=600,nWL=150, nWH=150):
        '''Use the first half for background study and the second half for signal extraction'''
        Nhalf = len(sample)/2
        ## The the average and RMS of the first half
        mean1 = nm.mean(sample[:Nhalf-nB])
        
        ## Get the second half after subtracting the background
        sample2 = [x-mean1 for x in sample[Nhalf+nS:]]

        ## get the avarage maximum of the second half, calculate the amplitude
        maxI2, max2 = max(enumerate(sample2), key=lambda p:p[1])
        ix = maxI2
        while sample2[ix]>0 and ix<len(sample2): ix += 1
        mean2 = nm.mean(sample2[max(maxI2-nWL,0):maxI2+nWH])
        if isDebug: print mean1,mean2,maxI2, max2

        return mean2
    def analysisMore(self, sample, nB=50, nS=600,nWL=150, nWH=150):
        '''Use the first half for background study and the second half for signal extraction'''
        Nhalf = len(sample)/2
        ## The the average and RMS of the first half
        mean1 = nm.mean(sample[:Nhalf-nB])
        
        ## Get the second half after subtracting the background
        sample2 = [x-mean1 for x in sample[Nhalf+nS:]]

        ## get the avarage maximum of the second half, calculate the amplitude
        maxI2, max2 = max(enumerate(sample2), key=lambda p:p[1])
        ix = maxI2
        while sample2[ix]>0 and ix<len(sample2): ix += 1
        mean2 = nm.mean(sample2[max(maxI2-nWL,0):maxI2+nWH])
        if isDebug: print mean1,mean2,maxI2, max2

        return mean2, maxI2, ix

class DeltaUScanner(dataTaker):
    def __init__(self,outFileName=None):
        dataTaker.__init__(self,outFileName)
        self.sampler = None
        self.fout = None

    def setup(self):
        self.connect()
        #0.0983856601469 1.22217230856 0.304039126696 0.427606878636 78.9207677012 74.8590110773 0.443751901382 0.0

        self.mic4.sReg.setPar('VCLIP' ,0.  , 0.689, 0x200)
        self.mic4.sReg.setPar('VReset',1.2, 0.703, 0x200)
        self.mic4.sReg.setPar('VCASN2',0.5, 0.693, 0x200)
        self.mic4.sReg.setPar('VCASN' ,0.4, 0.689, 0x200)
        self.mic4.sReg.setPar('VCASP' ,0.5, 0.694, 0x200)
        self.mic4.sReg.setPar('VRef'  ,0.4, 0.701, 0x200)
        self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
        self.mic4.sReg.setPar('IDB'   ,0xf0)
        self.mic4.sReg.setPar('ITHR'  ,0x80)
        self.mic4.sReg.setPar('IRESET',0x80)
        self.mic4.sReg.setPar('IDB2'  ,0x80)

# SUB=-3V Chip #5 bias1



#        self.mic4.sReg.setPar('VCLIP' ,0.37,  0.833, 0b1001011001)
#        self.mic4.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
#        self.mic4.sReg.setPar('VCASN2',0.8,  0.502, 0b101100110)
#        self.mic4.sReg.setPar('VCASN' ,0.76,  0.384, 0b100011110)
#        self.mic4.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
#        self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#        self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
#        self.mic4.sReg.setPar('IDB'   ,0x80)
#        self.mic4.sReg.setPar('ITHR'  ,0x80)
#        self.mic4.sReg.setPar('IRESET',0x80)
#        self.mic4.sReg.setPar('IDB2'  ,0x80)



# SUB=-3V Chip #5 bias2

# 
#         self.mic4.sReg.setPar('VCLIP' ,0.47,  0.833, 0b1001011001)
#         self.mic4.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
#         self.mic4.sReg.setPar('VCASN2',0.9,  0.502, 0b101100110)
#         self.mic4.sReg.setPar('VCASN' ,0.9,  0.384, 0b100011110)
#         self.mic4.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
#         self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#         self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
#         self.mic4.sReg.setPar('IDB'   ,0x80)
#         self.mic4.sReg.setPar('ITHR'  ,0x80)
#         self.mic4.sReg.setPar('IRESET',0x80)
#         self.mic4.sReg.setPar('IDB2'  ,0x80)

# SUB=-4V Chip #5 bias1


#         self.mic4.sReg.setPar('VCLIP' ,0.47,  0.833, 0b1001011001)
#         self.mic4.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
#         self.mic4.sReg.setPar('VCASN2',0.9,  0.502, 0b101100110)
#         self.mic4.sReg.setPar('VCASN' ,0.9,  0.384, 0b100011110)
#         self.mic4.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
#         self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#         self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
#         self.mic4.sReg.setPar('IDB'   ,0x80)
#         self.mic4.sReg.setPar('ITHR'  ,0x80)
#         self.mic4.sReg.setPar('IRESET',0x80)
#         self.mic4.sReg.setPar('IDB2'  ,0x80)


        self.mic4.sReg.setTRX16(0b1000)
        self.mic4.sReg.selectVolDAC(0)
        self.mic4.sReg.selectCurDAC(4)
        self.mic4.sReg.selectCol(12)

        self.mic4.sReg.show()
        self.mic4.testReg(read=True)

        self.mic4.s.settimeout(0.1)

    def measure_average(self, vH, vL, N=1):
        self.mic4.setVhVl(vH,vL)

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


    def measure(self, vH, vL):
        self.mic4.setVhVl(vH,vL)
        time.sleep(1)

        self.mic4.sendA_PULSE()
        time.sleep(1)
        self.wave.channel = 4
        sample = self.wave.getData()
        v,R,W = self.analysisMore(sample)

        self.wave.channel = 3
        sample1 = self.wave.getData()
        vout = 0
        for i in sample1:
            if i>0.5:
                vout = 1
                break

        print v,vout, R, W
        return v, vout, R, W

    def run_average(self, N=5):

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

    def run(self):
        fout = open(self.outFileName,'w') if self.outFileName else None
        ### loop over
        vL = 0.
        for i in range(37):
            vH = i*0.05
            mean,vout = self.measure(vH, vL)
            if fout:
                fout.write('{0:.2f} {1:.2f} {2:.4f} {3:d}\n'.format(vL, vH, mean, vout))
        vH = 1.8
        for i in range(37):
            vL = i*0.05
            mean,vout = self.measure(vH, vL)
            if fout:
                fout.write('{0:.2f} {1:.2f} {2:.4f} {3:d}\n'.format(vL, vH, mean, vout))

    def run2(self):
        fout = open(self.outFileName,'w') if self.outFileName else None
        ### loop over
        vL = 0.6
        for i in range(37):
            vH = vL + i*0.05
            if vH > 1.3: break
            mean,vout = self.measure(vH, vL)
            if fout:
                fout.write('{0:.2f} {1:.2f} {2:.4f} {3:d}\n'.format(vL, vH, mean, vout))

    def run3(self):
        fout = open(self.outFileName,'w') if self.outFileName else None
        ### loop over
        vL = 0.7
        for i in range(4):
            vH = 0.835 + i*0.01
            for j in range(100):
                mean,vout, R, W = self.measure(vH, vL)
                if fout:
                    fout.write('{6:d} {0:.4f} {1:.3f} {2:.4f} {3:d} {4:d} {5:d}\n'.format(vL, vH, mean, vout, R, W, j))

    def run4(self):
        fout = open(self.outFileName,'w') if self.outFileName else None
        ### loop over
        vL = 0.7
        for i in range(9):
            vH = 0.955 + i*0.005
            for j in range(100):
                mean,vout, R, W = self.measure(vH, vL)
                if fout:
                    fout.write('{6:d} {0:.4f} {1:.3f} {2:.4f} {3:d} {4:d} {5:d}\n'.format(vL, vH, mean, vout, R, W, j))


    def measureX(self, x):
        vL = self.vL
        vH = x+self.vL
        mean,vout, R, W = self.measure(vH, vL)
        if self.fout:
            self.fout.write('{6:d} {0:.4f} {1:.3f} {2:.4f} {3:d} {4:d} {5:d}\n'.format(vL, vH, mean, vout, R, W, 0))

        return vout

    def measureY(self,x):
        vL = self.vL
        vH = x+self.vL
        self.mic4.setVhVl(vH, vL)
        time.sleep(0.5)
        self.mic4.sendA_PULSE()
        fd = 0
        try:
            l1 = self.mic4.getFDAddresses()
            if len(l1)>1: print "more than 1 addresses"
            if l1: fd = l1.index((127,12)) >= 0 and 1 or 0
        except socket.timeout as e:
            print "caught the exception:", e
        print x, fd
        if self.fout:
            self.fout.write('{3:d} {0:.4f} {1:.4f} {2:d}\n'.format(vL, vH, fd,0))

        return fd

    def run5(self, N=700):
        self.fout = open(self.outFileName,'w') if self.outFileName else None
        self.vL = 0.7

        s1 = sampler((0.05,0.8),15)
        s1.funY = lambda x:math.sqrt(x*(1.-x))
        s1.funX = self.measureY
        s1.sFactor = 100
        s1.show()

        for i in range(N):
            s1.generate()

        self.fout.close()

def test_DeltaUScanner():
#     t1 = DeltaUScanner("scan2loops.dat")
#    t1 = DeltaUScanner("ENC_Chip5Col12_scan2.dat")
#    t1 = DeltaUScanner("Qth_0504_Chip5Col12_scan_sub-3v_bias2.dat")
#    t1 = DeltaUScanner("ENC_0504_Chip5Col12_scan_sub-3v_bias2.dat")
#    t1 = DeltaUScanner("Qth_0504_Chip5Col12_scan_sub-4v_bias1.dat")
#     t1 = DeltaUScanner("ENC_0504_Chip5Col12_scan_sub-4v_bias1.dat")
#     t1 = DeltaUScanner("ENC_0504_Chip5Col12_scan_sub-3v_bias2_try2.dat")
    t1 = DeltaUScanner("ENC_0507_Chip5Col12_scan_normal_try1.dat")
#     t1.wave.saveDataToFile = open('test112.dat','w')
#     t1.wave.channel = 4
    t1.setup()
#     t1.measure(1.3,0.6)
#     t1.saveDataToFile.close()
    t1.run5()

#    t1.run3()
#     t1.run4()

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

    def auto_tune_fun0(self,x):
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
            v = self.analysis(sample, nB=300, nS=800)
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

    def auto_tune_fun(self,x):
        '''The function that takes the parameters and return the score'''
        ### send the 200 bit reg to setup DAC -- DAC8568 should already have been set
        self.mic4.sReg.value =  0
        self.mic4.sReg.setPDB(0)
        ## chip-5
        self.mic4.sReg.setPar('VCLIP'   ,x[0],0.689, 0x200)
        self.mic4.sReg.setPar('VReset'  ,x[1],0.703, 0x200)
        self.mic4.sReg.setPar('VCASN2'  ,0.5 ,0.693, 0x200)
        self.mic4.sReg.setPar('VCASN'   ,x[2],0.689, 0x200)
        self.mic4.sReg.setPar('VCASP'   ,x[3],0.694, 0x200)
        self.mic4.sReg.setPar('VRef'    ,0.4 ,0.701, 0x200)
        self.mic4.sReg.setPar('IBIAS'   ,int(x[4]))
        self.mic4.sReg.setPar('IDB'     ,0x80)
        self.mic4.sReg.setPar('ITHR'    ,int(x[5]))
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
            v = self.analysis(sample, nB=300, nS=800)
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
    t1 = Tuner("tune_chip5_Row127_Col12_Apr28a_out2.dat")
    t1.wave.channel = 4
    t1.setup()
    t1.Col = 12
    t1.N = 1
#     t1.auto_tune_fun([0,1.1,0.5,0.4,0.6, 0xff, 0xf0, 0x80])
#     t1.setUpTest()
#     t1.atBounds = [(0,0.5),(0.5,1.49),(0.2,1.4),(0.3,1.0),(0.2,1.4),(0,0xff),(0,0xff),(0,0xff)]
    t1.atBounds = [(0,0.1),(0.8,1.3),(0.3,0.8),(0.3,0.7),(0x40,0xff),(0x40,0xff)]
    t1.tune()

if __name__ == '__main__':
#     runTune()
    test_DeltaUScanner()
