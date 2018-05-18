#!/usr/bin/env python
from ROOT import *
import random, math
from collections import defaultdict
# from rootUtil import waitRootCmdX, useAtlasStyle, get_default_fig_dir
import time, os
# import subprocess
import numpy as nm

gROOT.LoadMacro('encFitter.C+')
from ROOT import encFitter

import sys
sys.path.append('../../Control/src')
from MIC4Config import MIC4Config


def genList(l1, N, roundN=5):
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
    if roundN is not None: l3 = [round(x,roundN) for x in l3]

    return l3

def fillList(list1, maxStep=0.004, roundN=5):
    list2 = sorted(list1)
    n = len(list2)-1
    for i in range(n):
        if list2[i+1]-list2[i] > maxStep:
            nx = int((list2[i+1]-list2[i])/maxStep)
            step = (list2[i+1]-list2[i])/(nx+1)
#             print i, list2[i], list2[i+1], nx, step, list2, [list2[i]+(j+1)*step for j in range(nx)]
            list2 += [list2[i]+(j+1)*step for j in range(nx)]
    return [round(x,roundN) for x in sorted(list2)]

class ENCScanner:
    def __init__(self):
        self.fitter = encFitter()
        self.fitter.mean0 = -1
        self.fitter.sigma0 = -1
        self.npoints = 7
        self.nSamples1 = 10
        self.nSamples2 = 100
        self.nSamples3 = 50
        self.totalStats = defaultdict(int)
        self.passStats = defaultdict(int)
        self.workList = [0.,0.6]
        self.funX = None
        self.funY = None
        self.sigmaErrMax = 0.0003
        self.sigmaErrRelMax = 0.01
        self.nFitTry = 5
        self.nPixel = 1
        self.autoInitial = True

    def showStats(self):
        for dv in sorted(self.totalStats.iterkeys()):
            print dv, self.totalStats[dv], self.passStats[dv], float(self.passStats[dv])/self.totalStats[dv]
    def saveStats(self,fout,prefix='# '):
        for dv in sorted(self.totalStats.iterkeys()):
            fout.write(prefix+'{0:.5f} {1:d} {2:d} {3:.3f}\n'.format(dv, self.totalStats[dv], self.passStats[dv], float(self.passStats[dv])/self.totalStats[dv]))

    def doTest(self, dv, N=100):
        self.funX(dv)
        self.funY()
        for i in range(N):
            fd = self.funY()

            print i, fd
        

    def doScan(self):
        self.fitter.clearData()
        self.totalStats = defaultdict(int)
        self.passStats = defaultdict(int)
        ### first step, narrow down the region
        listA = [0.,0.6]
        while len(listA)<4:
#             print listA
            if len(listA) <2:
                print "Not a good range..... Skipping..."
                return
            listB = genList(listA, self.npoints)
            print 'Will scan', listB
            listA = []

            kx0 = None
            ### check the points of list B and update ListA
#             print "-"*20
            for dv in listB:
#                 print dv
                self.funX(dv)
                kx = 0
                for j in range(self.nSamples1):
                    fd = self.funY()
#                     print j,'----',fd
                    self.fitter.addData(dv, fd)
                    self.totalStats[dv] += 1
                    self.passStats[dv] += fd
                    kx += fd
#                 print kx, kx0, listA
                if kx0 is None: kx0 = kx
                if kx == kx0:
                    dv0 = dv
                else:
                    if len(listA)==0:
#                         print 'saving dv0=',dv0, 'kx =',kx,'kx0=',kx0
                        listA.append(dv0)
                    listA.append(dv)
                    kx0 = kx
#             print "="*20
            self.showStats()

        ### OK, now we have more than 3 points
        listC = genList(listA, self.npoints)
        for dv in listC:
            self.funX(dv)
            for j in range(self.nSamples2):
                fd = self.funY()
                self.fitter.addData(dv, fd)
                self.totalStats[dv] += 1
                self.passStats[dv] += fd
            print 'P = ',float(self.passStats[dv])/self.totalStats[dv]
        while True:
            if self.fitter.mean0 < 0 or self.autoInitial:
#                 self.fitter.mean0 = listC[len(listC)/2]
                Ys = [(dv, float(self.passStats[dv])/self.totalStats[dv]) for dv in self.totalStats]
                ### get sorted values
                st = sorted(Ys, key=lambda x:abs(x[1]-0.5))
                ### st[0] and st[1] should be close to value
                if abs(st[0][1] + st[1][1] - 1) < 0.2:
                    self.fitter.mean0 = st[0][0] + (st[1][0]-st[0][0])/(st[1][1]-st[0][1])*(0.5-st[0][1])
                else:
                    self.fitter.mean0 = st[0][0]

            if self.fitter.sigma0 < 0 or self.autoInitial:
#                 self.fitter.sigma0 = (listC[-1]-listC[0])/10.
                self.fitter.sigma0 = 0.005
            self.fitter.meanD = listC[0]
            self.fitter.meanU = listC[-1]
            self.fitter.sigmaD = (listC[-1]-listC[0])/1000.
            self.fitter.sigmaU = (listC[-1]-listC[0])/2.

            self.showStats()

            for itry in range(self.nFitTry):
                print itry, 'th try, initial values:', self.fitter.mean0, self.fitter.sigma0
                self.fitter.fit()
                if not math.isnan(self.fitter.mean): break
                self.fitter.sigma0 *= 2.

            if self.fitter.sigmaErr < self.sigmaErrMax or self.fitter.sigmaErr/self.fitter.sigma < self.sigmaErrRelMax: break

            for dv in listC: 
                self.funX(dv)
                for j in range(self.nSamples3):
                    fd = self.funY()
                    self.fitter.addData(dv, fd)
                    self.totalStats[dv] += 1
                    self.passStats[dv] += fd
                print 'P = ',float(self.passStats[dv])/self.totalStats[dv]

        return True

class pixelData:
    '''A class to hold the pixel data'''
    def __init__(self, address, fitter=None):
        self.addr = address
        self.fitter = fitter
        self.totalStats = defaultdict(int)
        self.passStats  = defaultdict(int)
        self.mean = -1
        self.sigma = -1
        self.meanErr = -1
        self.sigmaErr = -1
        self.cachedResults = None
    def D(self,list1,x=None):
        fd = 1 if (list1 is not None) and (self.addr in list1) else 0
        if x is not None:
            self.totalStats[x] += 1
            self.passStats[x]  += fd
            self.cachedResults = None
        return fd
    
    def mean_estimate(self):
        Ys = [(dv, float(self.passStats[dv])/self.totalStats[dv]) for dv in self.totalStats]
        ### get sorted values
        st = sorted(Ys, key=lambda x:abs(x[1]-0.5))
        ### st[0] and st[1] should be close to value
        if abs(st[0][1] + st[1][1] - 1) < 0.2:
            mean0 = st[0][0] + (st[1][0]-st[0][0])/(st[1][1]-st[0][1])*(0.5-st[0][1])
        else:
            mean0 = st[0][0]

        return mean0, 0.005

    def ENC(self):
        self.fitter.clearData()
        for dv,n in self.totalStats.items():
            for j in range(n):
                self.fitter.addData(dv, n<self.passStats[dv])
        self.fitter.mean0, self.fitter.sigma0 = self.mean_estimate() 
        self.fitter.fit()
        self.mean = self.fitter.mean
        self.meanErr = self.fitter.meanErr
        self.sigma = self.fitter.sigma
        self.sigmaErr = self.fitter.sigmaErr
        self.cachedResults = 1

    def encError(self):
        if self.cachedResults is None:
            self.ENC()
        return self.sigmaErr

    def meanError(self):
        if self.cachedResults is None:
            self.ENC()
        return self.meanErr
    def dumpInfo(self):
        text = '\n#---\n'
        text += '{0:d} {1:d} {2:.5g} {3:.5g} {4:.5g} {5:.5g}\n'.format(self.addr[0],self.addr[1],self.mean,self.meanErr,self.sigma,self.sigmaErr)
        for dv in sorted(self.totalStats.iterkeys()):
            text += '# {0:.5f} {1:d}  {2:d}\n'.format(dv, self.totalStats[dv], self.passStats[dv])
        return text

class multiPixelENC:
    def __init__(self):
        self.fitter = encFitter()
        self.pixels = [pixelData((i,j),self.fitter) for i in range(120,128) for j in range(32)]
        self.funX = self.setDU
        self.funY = self.getVal
        self.npoints = 10
        self.nSamples1 = 1
        self.nSamples2 = 120
        self.nSamples3 = 50
        self.rangeY0 = 0.01
        self.rangeY1 = 0.99
        self.enc_error_MAX = 0.0003
        self.outfilename = 'test_muitipixelECN.dat'
        self.mic4 = MIC4Config()
        self.vL = 0.7

        self.nCheck = 10
        self.checkList = self.getCheckList(self.nCheck)

    def setup(self):
        self.mic4.setup(configID=0)

    def getCheckList(self,n, update=False):
        if update: self.nCheck = n
        step = len(self.pixels)/n
        self.pCheck = self.pixels[::step] if step>0 else self.pixels

    def setDU(self, dU):
        '''Same as 1 pixel case'''
        self.dU = dU
        self.mic4.setVhVl(self.vL+dU, self.vL)
        time.sleep(0.2)
        self.mic4.getFDAddresses(100, True) ### make sure the FIFO is empty...

    def check(self, list1):
        '''Used to check the health of the returned addresses. 1) duplication; 2) validate'''
        if len(list1)==0: print "Empty list, wrong header?"
        jd = defaultdict(int)
        for x in list1:
            jd[x] += 1
        for x in jd:
            if jd[x]>1:
                print "duplicated:",x,' --> ', jd[x]
            if jd[x]>5:
#                 self.mic4.setPixels([(x[0],x[1],1,0)])                
                self.mic4.sendGRST_B()
                print "reset the states"

    def getVal(self):
        '''Use some pixels to calculate, no need to do all of them
        The statistics need to be recorded.
        '''
        self.mic4.getFDAddresses(100) # empty fifo
        self.mic4.sendA_PULSE()
        time.sleep(0.05)

        adds = self.mic4.getFDAddresses(100,debug=1)
#         print adds
        if adds is not None: self.check(adds)
        return sum([p.D(adds, self.dU) for p in self.pixels])

    def get_enc_error(self, n):
        step = len(self.pixels)/n
        if step < 1: step = 1
        return nm.mean([p.encError() for p in self.pixels[::step]])

    def showStats(self):
        for dv in sorted(self.totalStats.iterkeys()):
            print dv, self.totalStats[dv], self.passStats[dv], float(self.passStats[dv])/self.totalStats[dv]
    def saveStats(self,fout,prefix='# '):
        for dv in sorted(self.totalStats.iterkeys()):
            fout.write(prefix+'{0:.5f} {1:d} {2:d} {3:.3f}\n'.format(dv, self.totalStats[dv], self.passStats[dv], float(self.passStats[dv])/self.totalStats[dv]))

    def run_check(self):
        ''' the main function...'''
        ### preparation
        self.totalStats = defaultdict(int)
        self.passStats = defaultdict(int)
        listA = [0.,0.6]
        npixel = len(self.pixels)

        ### Find a good range to take data. We can do 10 points
        while len(listA)<4:
            if len(listA) <2:
                print "Not a good range..... Skipping..."
                return
            listB = genList(listA, self.npoints)
            print 'Will scan', listB
            listA = []

            listL = [listB[0]]
            listH = [listB[-1]]
            ### check the points of list B and update ListA
            for dv in listB:
                self.funX(dv)
                for j in range(self.nSamples1):
                    fd = self.funY()
                    self.totalStats[dv] += npixel
                    self.passStats[dv] += fd
                    r = float(self.passStats[dv])/self.totalStats[dv]
                    if r < self.rangeY0:
                        listL.append(dv)
                    elif r>self.rangeY1:
                        listH.append(dv)
                    else: listA.append(dv)
            listA += [max(listL), min(listH)]

            self.showStats()

        ### OK, now we have more than 3 points
        ### Take data until enough
        print "going with", listA
        listC = fillList(genList(listA, self.npoints),0.003)
        print 'Will scan', listC
        nSample = self.nSamples2
        while True:
            for dv in listC: 
                self.funX(dv)
                for j in range(nSample):
                    fd = self.funY()
                    self.totalStats[dv] += npixel
                    self.passStats[dv] += fd
                print 'P = ',float(self.passStats[dv])/self.totalStats[dv]

            if self.enc_error_MAX is None or self.get_enc_error(10) < self.enc_error_MAX: break
            nSample = self.nSamples3

        ### Save data for further analysis
        ### for each pixel
        with open(self.outfilename, 'w') as fout1:
            for p in self.pixels:
                fout1.write(p.dumpInfo())

    def report(self):
        for p in self.pixels:
            p.ENC()
            print p.addr, p.mean, p.meanErr, p.sigma, p.sigmaErr


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
        self.vL = 0.7
        self.logFile = None

    def setDU(self, dU):
        self.mic4.setVhVl(self.vL+dU, self.vL)
        time.sleep(0.2)
        self.mic4.getFDAddresses(100, True) ### make sure the FIFO is empty...
    def getVal(self):
        self.mic4.sendA_PULSE()
        time.sleep(0.05)
        addrs = self.mic4.getFDAddresses(100)
#         addrs = self.mic4.getFDAddresses(100, True)
        print addrs
        return 0 if addrs is None or self.pixel not in addrs else 1
    def scanX(self):
        self.mic4.setup()

        cx1 = ENCScanner()
        cx1.funX = self.setDU
        cx1.funY = self.getVal
#SUB=0V
#        for i in range(1):
#            ix = 0.4+0.1*i
#            #if ix > 0.7 : break
#            vclip = 0.
#            vcasn = ix
#            vcasp = 0.5
#            vreset= 1.35
#            vcasn2= 0.5
#            vref  = 0.4
#            ibias = 0xff
#            idb   = 0x80
#            ithr  = 0x70
#            ireset= 0x80
#            idb2  = 0x80
#SUB=-3V
        for i in range(15):
            ix = 0x20+16*i
            #if ix > 1.4 : break
            vclip = 0.45
            vcasn = 0.87
            vcasp = 0.5
            vreset= 1.4
            vcasn2= 0.9
            vref  = 0.4
            ibias = 0xff
            idb   = 0x80
            ithr  = ix  #0x80
            ireset= 0x80
            idb2  = 0x80

            ### set the values
            self.mic4.sReg.setPar('VCLIP' ,vclip,   0.686, 0x200) #select<5>
            self.mic4.sReg.setPar('VReset',vreset,   0.701, 0x200) #select<2> 
            self.mic4.sReg.setPar('VCASN2',vcasn2,   0.692, 0x200) #select<1>
            self.mic4.sReg.setPar('VCASN' ,vcasn,  0.695, 0x200) #select<4>
            self.mic4.sReg.setPar('VCASP' ,vcasp,  0.692, 0x200) #select<3>
            self.mic4.sReg.setPar('VRef'  ,vref,    0.701, 0x200) #select<0> 
            self.mic4.sReg.setPar('IBIAS' ,ibias )#select<4> 0x80 is 0.342  0xff is 0.588
            self.mic4.sReg.setPar('IDB'   ,idb   )#select<6> 0x80 is 0.0738 0xff is 0.1154 0xc0 is 0.101
            self.mic4.sReg.setPar('ITHR'  ,ithr  )#select<5> 0x80 is 0.0101 0xff is 0.0158 0x40 is 6.4mV
            self.mic4.sReg.setPar('IRESET',ireset)
            self.mic4.sReg.setPar('IDB2'  ,idb2  )

# SUB=-3V Chip #5 bias6

 
#         self.mic4.sReg.setPar('VCLIP' ,0.45,  0.686, 0x200) #select<5>
#         self.mic4.sReg.setPar('VReset',1.388,  0.701, 0x200) #select<2> 
#         self.mic4.sReg.setPar('VCASN2',0.9,  0.692, 0x200) #select<1>
#         self.mic4.sReg.setPar('VCASN' ,0.87,  0.695, 0x200) #select<4>
#         self.mic4.sReg.setPar('VCASP' ,0.5,  0.692, 0x200) #select<3>
#         self.mic4.sReg.setPar('VRef'  ,0.4,  0.701, 0x200) #select<0> 
#         self.mic4.sReg.setPar('IBIAS' ,0xff) #select<4> 0x80 is 0.342  0xff is 0.588
#         self.mic4.sReg.setPar('IDB'   ,0x80) #select<6> 0x80 is 0.0738 0xff is 0.1154 0xc0 is 0.101
#         self.mic4.sReg.setPar('ITHR'  ,0x40) #select<5> 0x80 is 0.0101 0xff is 0.0158 0x40 is 6.4mV
#         self.mic4.sReg.setPar('IRESET',0x80)
#         self.mic4.sReg.setPar('IDB2'  ,0x80)






#             self.mic4.sReg.setPar('VCLIP' ,vclip,   0.833, 0b1001011001)
#             self.mic4.sReg.setPar('VCASN' ,vcasn,   0.384, 0b100011110 )
#             self.mic4.sReg.setPar('VCASP' ,vcasp,   0.603, 0b110110000 )
#             self.mic4.sReg.setPar('VReset',vreset,  1.084, 0b1100000111)
#             self.mic4.sReg.setPar('VCASN2',vcasn2,  0.502, 0b101100110 )
#             self.mic4.sReg.setPar('VRef'  ,vref,    0.406, 0b100011111 )
#             self.mic4.sReg.setPar('IBIAS' ,ibias )
#             self.mic4.sReg.setPar('IDB'   ,idb   )
#             self.mic4.sReg.setPar('ITHR'  ,ithr  )
#             self.mic4.sReg.setPar('IRESET',ireset)
#             self.mic4.sReg.setPar('IDB2'  ,idb2  )

            self.mic4.sReg.selectVolDAC(2)
            self.mic4.sReg.selectCurDAC(6)
            self.mic4.sReg.selectCol(12)
            self.mic4.sReg.setTRX16(0b1000)
            self.mic4.sReg.show()
            self.mic4.testReg(read=True)

            ### empty fifo first
            self.mic4.getFDAddresses(100)

#             cx1.doTest(0.2)
#             return

#             if cx1.fitter.mean0< 0: cx1.fitter.mean0 = 0.136
#             if cx1.fitter.sigma0<0: cx1.fitter.sigma0 = 0.005
            ### the results of ENC
            cx1.doScan()
            print i, ix, cx1.fitter.mean, cx1.fitter.meanErr, cx1.fitter.sigma, cx1.fitter.sigmaErr
            
            cx1.fitter.mean0 = cx1.fitter.mean
            cx1.fitter.sigma0 = cx1.fitter.sigma

            if self.logFile:
                self.logFile.write('#- VCLIP={0:.4f},VCASN={1:.4f},VCASP={2:.4f},VCRESET={3:.4f},VCASN2={4:.4f},VREF={5:.4f},IBIAS=0x{6:X},IDB=0x{7:X},ITHR=0x{8:X},IRESET=0x{9:X},IDB2=0x{10:X}\n'.format(vclip,vcasn,vcasp,vreset,vcasn2,vref,ibias,idb,ithr,ireset,idb2))
                self.logFile.write('{0:d} {1:.4f} {2:.6f} {3:.6f} {4:.6f} {5:.6f}\n'.format(i,ix,cx1.fitter.mean, cx1.fitter.meanErr, cx1.fitter.sigma, cx1.fitter.sigmaErr))
                cx1.saveStats(self.logFile)
                self.logFile.flush()


def testScan():
    mc1 = mic4ENCCalculator()
    mc1.pixel = (127,12)
#    logFileName = 'DAC_scan_vcasn_0p2to0p6.dat'
    logFileName = 'May18_ENC_col12_SUB-3V_scan_ithr_0x20to0xf0.dat'
    if os.path.exists(logFileName):
        idz = 1
        while os.path.exists(logFileName+'.'+str(idz)):
            idz += 1
        logFileName += '.'+str(idz)

    with open(logFileName,'w') as f1:
        mc1.logFile = f1
        mc1.scanX()


def checkFit():
    data='''
# 0.0 20 0 0.0
# 0.1 40 0 0.0
# 0.116666666667 40 1 0.025
# 0.119444444444 10 0 0.0
# 0.122222222222 170 3 0.0176470588235
# 0.125 160 10 0.0625
# 0.127777777778 170 28 0.164705882353
# 0.130555555556 150 35 0.233333333333
# 0.130555555556 10 9 0.9
# 0.133333333333 190 92 0.484210526316
# 0.136111111111 150 89 0.593333333333
# 0.138888888889 160 138 0.8625
# 0.144444444444 10 10 1.0
# 0.15 30 30 1.0
# 0.166666666667 20 20 1.0
# 0.183333333333 20 20 1.0
# 0.2 20 20 1.0
# 0.2 20 20 1.0
# 0.3 20 20 1.0
# 0.4 20 20 1.0
# 0.5 20 20 1.0
# 0.6 20 20 1.0

0.0 20 0 0.0
0.01667 10 0 0.0
0.03333 10 0 0.0
0.05 10 0 0.0
0.06667 10 0 0.0
0.08333 20 0 0.0
0.08611 110 1 0.00909090909091
0.08889 110 8 0.0727272727273
0.09028 100 5 0.05
0.09167 110 23 0.209090909091
0.09444 110 44 0.4
0.09722 110 73 0.663636363636
0.1 130 118 0.907692307692
0.2 10 10 1.0
0.3 10 10 1.0
0.4 10 10 1.0
0.5 10 10 1.0
0.6 10 10 1.0
# 
# 0.0 10 0 0.0
# 0.1 130 0 0.0
# 0.10278 100 3 0.03
# 0.10556 110 19 0.172727272727
# 0.11111 110 74 0.672727272727
# 0.11389 100 89 0.89
# 0.11667 120 114 0.95
# 0.12222 110 110 1.0
# 0.12778 10 10 1.0
# 0.13333 20 20 1.0
# 0.15 10 10 1.0
# 0.16667 10 10 1.0
# 0.18333 10 10 1.0
# 0.2 20 20 1.0
# 0.3 10 10 1.0
# 0.4 10 10 1.0
# 0.5 10 10 1.0
# 0.6 10 10 1.0
# 
# 0.0 10 0 0.0
# 0.1 20 0 0.0
# 0.11667 20 0 0.0
# 0.11945 110 3 0.0272727272727
# 0.12222 110 15 0.136363636364
# 0.12361 100 11 0.11
# 0.125 110 34 0.309090909091
# 0.12639 100 41 0.41
# 0.12778 110 55 0.5
# 0.13055 110 88 0.8
# 0.13333 20 19 0.95
# 0.15 10 10 1.0
# 0.16667 10 10 1.0
# 0.18333 10 10 1.0
# 0.2 20 20 1.0
# 0.3 10 10 1.0
# 0.4 10 10 1.0
# 0.5 10 10 1.0
# 0.6 10 10 1.0

# 0.0 10 0 0.0
# # 0.1 30 1 0.0333333333333
# 0.10556 10 0 0.0
# 0.11111 10 0 0.0
# 0.11667 10 2 0.2
# 0.12222 10 4 0.4
# 0.12778 10 9 0.9
# 0.13333 20 20 1.0
# 0.16667 10 10 1.0
# # 0.2 20 12 0.6
# 0.23333 10 10 1.0
# 0.26667 10 10 1.0
# 0.3 20 20 1.0
# 0.4 10 10 1.0
# 0.5 10 10 1.0
# 0.6 10 10 1.0

# 
# 0.0 20 0 0.0
# 0.1 40 0 0.0
# 0.116666666667 40 0 0.0
# 0.119444444444 10 1 0.1
# 0.122222222222 170 0 0.0
# 0.125 10 1 0.1
# 0.127777777778 170 8 0.0470588235294
# 0.130555555556 150 3 0.02
# 0.130555555556 10 7 0.7
# 0.133333333333 190 39 0.205263157895
# 0.136111111111 150 48 0.32
# 0.138888888889 160 81 0.50625
# 0.144444444444 160 141 0.88125
# 0.15 30 30 1.0
# 0.166666666667 20 20 1.0
# 0.183333333333 20 20 1.0
# 0.2 20 20 1.0
# 0.2 20 20 1.0
# 0.3 20 20 1.0
# 0.4 20 20 1.0
# 0.5 20 20 1.0
# 0.6 20 20 1.0
'''
    en1 = encFitter()
    for d in data.split('\n'):
        d = d.rstrip()
        if len(d)==0 or d[0]=='#':
            continue
        fs = d.split()
        x = float(fs[0])
        npass = int(fs[2])
        for i in range(int(fs[1])):
            en1.addData(x,i<npass)
# 0.121369309723 0.00424943258986
# 0.0808686986566 0.015657313168
    en1.mean0 = 0.085
#     en1.sigma0 = 0.00424943258986
    en1.sigma0 = 0.015657313168

    en1.fit()

def testT():
    cx1 = ENCScanner() 
    g1 = GenXY()
#     g1.test()
    cx1.funX = g1.setX
    cx1.funY = g1.getY

    cx1.doScan()
    print cx1.fitter.mean, cx1.fitter.meanErr
    print cx1.fitter.sigma, cx1.fitter.sigmaErr

def testScanMore():
    a = multiPixelENC()
    a.setup()
    a.nSamples2 = 200
    a.enc_error_MAX = None
    a.outfilename = 'enc_scan_BlockRow15.dat'
    a.run_check()

        ###
if __name__== '__main__':
#     testT()
#     testScan()
    testScanMore()
#     print fillList([0.1,0.13,0.18,0.19],0.003)
#     checkFit()
#     x1 = genList([0.,1.],21)
#     print len(x1), x1
#     x2 = genList([0.,0.35,0.8,1.],21)
#     print len(x2), x2
