#!/usr/bin/env python
from ROOT import *
import random, math
from collections import defaultdict
# from rootUtil import waitRootCmdX, useAtlasStyle, get_default_fig_dir

gROOT.LoadMacro('encFitter.C+')
from ROOT import encFitter

import sys
sys.path.append('../../Control/src')
from MIC4Config import MIC4Config


def genList(l1, N):
    if len(l1)>=N: return l1

    l3 = None
    if len(l1)==2:
        step = (l1[-1]-l1[0])/(N-1)
        l3 = [l1[0]+i*step for i in range(N)]
    else:
        l2 = sorted(l1)
        ### distribute the points
        Ns = [1]*(len(l2)-1)
        while sum(Ns)< N+len(l1)-2:
            maxI, maxV = max(enumerate([(l2[i+1]-l2[i])/Ns[i] for i in range(len(l2)-1)]), key=lambda p:p[1])
            Ns[maxI] += 1
        l3 = []
        for i in range(len(l2)-1):
            l3 += [l2[i]+(l2[i+1]-l2[i])/(Ns[i]-1)*j for j in range(Ns[i]-1)]
        l3 += l2[-1:]
    return l3


class ENCScanner:
    def __init__(self):
        self.fitter = encFitter()
        self.fitter.mean0 = -1
        self.fitter.sigma0 = -1
        self.npoints = 10
        self.nSamples1 = 10
        self.nSamples2 = 100
        self.nSamples3 = 20
#         self.nSamplesX = self.nSamples1
#         self.mic4 = None
#         self.vL = 0.7
        self.totalStats = defaultdict(int)
        self.passStats = defaultdict(int)
        self.workList = [0.,0.6]
        self.funX = None
        self.funY = None
        self.sigmaErrMax = 0.0003

    def doScan(self):
        ### first step, narrow down the region
        listA = [0,0.6]
        while len(listA)<4:
            print listA
            listB = genList(listA, self.npoints)
            print listB
            listA = []

            kx0 = None
            ### check the points of list B and update ListA
            print "-"*20
            for dv in listB:
                print dv
                self.funX(dv)
#                 vH = self.vL + dv
#                 self.mic4.setVhVl(vH, self.vL)
                kx = 0
                for j in range(self.nSamples1):
                    fd = self.funY()
#                     self.mic4.sendA_Pulse()
#                     fd = getResultsXXX
                    self.fitter.addData(dv, fd)
                    self.totalStats[dv] += 1
                    self.passStats[dv] += fd
                    kx += fd
                print kx, kx0, listA
                if kx0 is None: kx0 = kx
                if kx == kx0:
                    dv0 = dv
                else:
                    if len(listA)==0: listA.append(dv0)
                    listA.append(dv)
                    kx0 = kx
            print "="*20
#         return
        ### OK, now we have more than 3 points
        listC = genList(listA, self.npoints)
        for dv in listC:
            self.funX(dv)
#             vH = self.vL + dv
#             self.mic4.setVhVl(vH, self.vL)
            for j in range(self.nSamples2):
                fd = self.funY()
#                 self.mic4.sendA_Pulse()
#                 fd = getResultsXXX
                self.fitter.addData(dv, fd)
                self.totalStats[dv] += 1
                self.passStats[dv] += fd
        while True:
            if self.fitter.mean0 < 0:
                self.fitter.mean0 = listC[len(listC)/2]
            if self.fitter.sigma0 < 0:
                self.fitter.sigma0 = (listC[-1]-listC[0])/2.

            self.fitter.fit()
            if self.fitter.sigmaErr < self.sigmaErrMax: break

            for dv in listC: 
                self.funX(dv)
#                 vH = self.vL + dv
#                 self.mic4.setVhVl(vH, self.vL)
                for j in range(self.nSamples3):
                    fd = self.funY()
#                     self.mic4.sendA_Pulse()
#                     fd = getResultsXXX
                    self.fitter.addData(dv, fd)
                    self.totalStats[dv] += 1
                    self.passStats[dv] += fd

#         for dv in sort(self.totalStats.keys):
#             print dv, self.totalStats[dv], self.passStats[dv], float(self.passStats[dv])/self.totalStats[dv]
        return


        return True

class GenXY:
    def __init__(self):
        self.fun1 = lambda x: 0.5*(1+math.erf((x-0.3)/(math.sqrt(2)*0.007)))
        self.x = 0
    def getY(self):
        return 0 if random.random()>self.fun1(self.x) else 1
    def setX(self,x):
        self.x = x
    def test(self):
        for i in range(20):
            self.setX(i*0.05)
            print i, i*0.05, self.getY()

class mic4ENCCalculator:
    def __init__(self):
        self.mic4 = MIC4Config()
        self.pixel = (127,12)

    def setDU(self, dU):
        self.mic4.setVhVl(self.vL+dU, self.vL)
    def getVal(self):
        addrs = self.mic4.getFDAddresses()
        return 1 if self.pixel in addrs else 0
    def scanX(self):
        self.mic4.setup()

        cx1 = ENCScanner()
        cx1.funX = self.setDU
        cx1.funY = self.getVal

        for i in range(10):
            ### set the values
            self.mic4.sReg.setPar('VCLIP' ,0,  0.833, 0b1001011001)
            self.mic4.sReg.setPar('VCASN' ,0.4,  0.384, 0b100011110)
            self.mic4.sReg.setPar('VCASP' ,0.5,  0.603, 0b110110000)
            self.mic4.sReg.setPar('VReset',1.2,  1.084, 0b1100000111)
            self.mic4.sReg.setPar('VCASN2',0.5,  0.502, 0b101100110)
            self.mic4.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
            self.mic4.sReg.setPar('IBIAS' ,0x80+0x10*i)
            self.mic4.sReg.setPar('IDB'   ,0x80)
            self.mic4.sReg.setPar('ITHR'  ,0x80)
            self.mic4.sReg.setPar('IRESET',0x80)
            self.mic4.sReg.setPar('IDB2'  ,0x80)

            self.mic4.sReg.selectVolDAC(2)
            self.mic4.sReg.selectCurDAC(6)
            self.mic4.sReg.setTRX16(0b1000)
            self.mic4.sReg.show()
            self.mic4.testReg(read=True)

            ### the results of ENC
            cx1.doScan()
            print i, ix, cx1.fitter.mean, cx1.fitter.meanErr, cx1.fitter.sigma, cx1.fitter.sigmaErr


def testScan():
    mc1 = mic4ENCCalculator()
    mc1.scanX()


def testT():
    cx1 = ENCScanner() 
    g1 = GenXY()
#     g1.test()
    cx1.funX = g1.setX
    cx1.funY = g1.getY

    cx1.doScan()
    print cx1.fitter.mean, cx1.fitter.meanErr
    print cx1.fitter.sigma, cx1.fitter.sigmaErr

        ###
if __name__== '__main__':
    testT()
#     x1 = genList([0.,1.],21)
#     print len(x1), x1
#     x2 = genList([0.,0.35,0.8,1.],21)
#     print len(x2), x2
