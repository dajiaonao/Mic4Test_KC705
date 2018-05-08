#!/usr/bin/env python
from ROOT import *

# gSystem.Load('encFitter.C+')
gROOT.LoadMacro('encFitter.C+')
from ROOT import encFitter

import sys
sys.path.append('../../Control/src')
from MIC4Config import MIC4Config

def getENC():
    ### set DAC

    ### Calculate ENC
    ## first scan
    N = 10
    Range0 = [0.05,0.8]
    Range = Range0
    d = (Range[1]-Range[0])/N
    for i in range(N+1):
        x = Range[0]+i*d
        vH = vL+x

        mic4.setVhVl(vH, vL)

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
    # en1.data1.push_back((0.1,0))
    # en1.data1.push_back((0.2,0))
    # en1.data1.push_back((0.3,0))
    # en1.data1.push_back((0.33,1))
    # en1.data1.push_back((0.35,0))
    # en1.data1.push_back((0.4,1))
    # en1.data1.push_back((0.5,1))
    # en1.data1.push_back((0.6,1))
    # en1.data1.push_back((0.7,1))
    # 
    # en1.fit()
    # print en1.mean, en1.sigma

    en1.test()

if __name__ == '__main__':
    testFitter()
