#!/usr/bin/env python
from PyDE import *
from MIC4Config import MIC4Config
import socket
import time
import numpy as nm

class WaveFormGetter:
    def __init__(self):
        self.hostname = "192.168.2.4"                #wire network hostname
        self.port = 5025                             #host tcp port

    def connect(self):
        ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
        ss.connect((self.hostname,self.port))                                 #connect to the server
        ss.send("*IDN?;")                           #read back device ID
        print "Connected to Instrument with ID: %s"%ss.recv(128)   

    def getData(self):
        ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
        Y_Range = float(ss.recv(128)[1:])   
        print "YRange:%f"%Y_Range
        #Y_Factor = Y_Range/980.0
        Y_Factor = Y_Range/62712.0
        #print Y_Factor

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
        sample = [0]*length/2
        for i in xrange(length/2):              #store data into file
            ### combine two words to form the number
            digital_number = (ord(totalContent[3+i*2+1])<<8)+ord(totalContent[3+i*2])
            if (ord(totalContent[3+i*2+1]) & 0x80) == 0x80:             
                sample[i] = (digital_number - 65535+1000)*Y_Factor + CH1_Offset
            else:
                sample[i] = (digital_number+1000)*Y_Factor + CH1_Offset
        return sample
    def showSample(self,sample):
        '''Check the sample, for debug'''
        pass


class Tuner:
    def __init__(self):
        self.Col = 0
        self.VolDAC = 0
        self.CurDAC = 0
        self.atBounds = None
        self.atMaxIters = 100
        self.mic4 = MIC4Config()
        self.wave = WaveFormGetter()

    def setup(self):
        self.mic4.connect()
        self.mic4.test_DAC8568_config()
        self.wave.connect()

    def tune(self):
        de = DE(self.auto_tune_fun, self.atBounds, maxiters=self.atMaxIters)
        ret = de.solve()
        print(ret)

    def auto_tune_fun(self,x):
        '''The function that takes the parameters and return the score'''
        val = 0.
        ### send the 200 bit reg to setup DAC -- DAC8568 should already have been set
        self.mic4.sReg.value =  0
        self.mic4.sReg.setPDB(0)
        self.mic4.sReg.setPar('VCLIP'   ,x[0], 0.075,0b0000101001)
        self.mic4.sReg.setPar('VReset'  ,x[1], 0.484,0b0101010101)
        self.mic4.sReg.setPar('VCASN2'  ,x[2], 0.57, 0b0110011001)
        self.mic4.sReg.setPar('VCASN'   ,x[3], 0.381,0b0100010001)
        self.mic4.sReg.setPar('VCASP'   ,x[4],1.040,0b1011101110)
        self.mic4.sReg.setPar('VRef'    ,0.4 , 0.4, 0b100011111)
        self.mic4.sReg.setPar('IBIAS'   ,x[5])
        self.mic4.sReg.setPar('IDB'     ,x[6])
        self.mic4.sReg.setPar('ITHR'    ,x[7])
        self.mic4.sReg.setPar('IRESET'  ,0x80)
        self.mic4.sReg.setPar('IDB2'    ,0x80)
        self.mic4.sReg.selectVolDAC(self.VolDAC)
        self.mic4.sReg.selectCurDAC(self.CurDAC)
        self.mic4.sReg.selectCol(self.Col)

        self.mic4.sReg.show()
        self.mic4.testReg(read=True)

        time.sleep(1)
        self.mic4.sendA_PULSE()

        ### get the waveform and analysis it
        sample = self.wave.getData()

        val = self.analysis(sample)
        return val

    def analysis(self, sample):
        '''Use the first half for background study and the second half for signal extraction'''
        Nhalf = len(sample)/2
        ## The the average and RMS of the first half
        mean1 = nm.mean(sample[:Nhalf])
        
        ## Get the second half after subtracting the background
        sample2 = [x-mean1 for x in sample[Nhalf:]]

        ## get the avarage maximum of the second half, calculate the amplitude
        maxI2, max2 = max(enumerate(sample2), key=lambda p:p[1])
        mean2 = nm.mean(sample2[maxI2-10, maxI2+10])

        return mean2

    def setUpTest(self):
        self.atBounds = [(-10,10)]

def runTune():
    t1 = Tuner()
    t1.setup()
    t1.setUpTest()
    t1.tune()

if __name__ == '__main__':
    runTune()
