#!/usr/bin/env python
from ROOT import *

gROOT.LoadMacro('encFitter.C+')
from ROOT import encFitter

import sys
sys.path.append('../../Control/src')
from MIC4Config import MIC4Config

class ENCChecker:
    def __init__(self):
        self.mic4 = MIC4Config()
    def setup(self, conifgID=50):
        self.mic4.connect()

        if configID == 50:
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

        elif configID == 51:
            # SUB=-3V Chip #5 bias1
            self.mic4.sReg.setPar('VCLIP' ,0.37,  0.833, 0b1001011001)
            self.mic4.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
            self.mic4.sReg.setPar('VCASN2',0.8,  0.502, 0b101100110)
            self.mic4.sReg.setPar('VCASN' ,0.76,  0.384, 0b100011110)
            self.mic4.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
            self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
            self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
            self.mic4.sReg.setPar('IDB'   ,0x80)
            self.mic4.sReg.setPar('ITHR'  ,0x80)
            self.mic4.sReg.setPar('IRESET',0x80)
            self.mic4.sReg.setPar('IDB2'  ,0x80)

        elif configID == 52:
            # SUB=-3V Chip #5 bias2
            self.mic4.sReg.setPar('VCLIP' ,0.47,  0.833, 0b1001011001)
            self.mic4.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
            self.mic4.sReg.setPar('VCASN2',0.9,  0.502, 0b101100110)
            self.mic4.sReg.setPar('VCASN' ,0.9,  0.384, 0b100011110)
            self.mic4.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
            self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
            self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
            self.mic4.sReg.setPar('IDB'   ,0x80)
            self.mic4.sReg.setPar('ITHR'  ,0x80)
            self.mic4.sReg.setPar('IRESET',0x80)
            self.mic4.sReg.setPar('IDB2'  ,0x80)

        elif configID == 53:
            # SUB=-4V Chip #5 bias1
            self.mic4.sReg.setPar('VCLIP' ,0.47,  0.833, 0b1001011001)
            self.mic4.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
            self.mic4.sReg.setPar('VCASN2',0.9,  0.502, 0b101100110)
            self.mic4.sReg.setPar('VCASN' ,0.9,  0.384, 0b100011110)
            self.mic4.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
            self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
            self.mic4.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V
            self.mic4.sReg.setPar('IDB'   ,0x80)
            self.mic4.sReg.setPar('ITHR'  ,0x80)
            self.mic4.sReg.setPar('IRESET',0x80)
            self.mic4.sReg.setPar('IDB2'  ,0x80)
        else:
            print "No configuration found for id:", configID


        self.mic4.sReg.setTRX16(0b1000)
        self.mic4.sReg.selectVolDAC(0)
        self.mic4.sReg.selectCurDAC(4)
        self.mic4.sReg.selectCol(12)

        self.mic4.sReg.show()
        self.mic4.testReg(read=True)

        self.mic4.s.settimeout(0.1)

    def getENC(self):
        ### Calculate ENC
        ## first scan
        N = 10
        M = 10
        Range0 = [0.05,0.8]
        Range = Range0
        d = (Range[1]-Range[0])/N
        for i in range(N+1):
            x = Range[0]+i*d
            vH = vL+x
            self.mic4.setVhVl(vH, vL)

            for i in range(M):
                mic4.sendA_Pulse()

                fd = getReasults
                en1.data1.push_back(x,fd)
        en1.fit()
        print en1.mean, en1.sigma
        if en1.sigmaErr>0.0005:
            # update the range
            Range = [max(en1.mean-en1.meanErr-3*(en1.sigma+en1.sigmaErr),Range0[0]), min(en1.mean+en1.meanErr+3*(en1.sigma+en1.sigmaErr),Range0[1])]

         ### record the results
         # DAC values, ENC values

def testFitter():
    en1 = encFitter()
    en1.addData(0.1,0)
    en1.addData(0.2,0)
    en1.addData(0.3,0)
    en1.addData(0.33,1)
    en1.addData(0.35,0)
    en1.addData(0.4,1)
    en1.addData(0.5,1)
    en1.addData(0.6,1)
    en1.addData(0.7,1)
    
    en1.fit()
    print en1.mean, en1.sigma

#     en1.test()

def test2():
    en1 = ENCChecker()
    en1.setup(50)
    en1.getENC()


if __name__ == '__main__':
    testFitter()
#     test2()
