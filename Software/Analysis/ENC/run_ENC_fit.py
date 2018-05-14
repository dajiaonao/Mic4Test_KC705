#!/usr/bin/env python
from ROOT import *
from rootUtil import waitRootCmdX, useAtlasStyle, get_default_fig_dir

gROOT.LoadMacro('encFitter.C+')
from ROOT import encFitter

import sys
sys.path.append('../../Control/src')
from MIC4Config import MIC4Config

<<<<<<< HEAD

sDir = get_default_fig_dir()

def getENC():
    ### set DAC
=======
class ENCChecker:
    def __init__(self):
        self.mic4 = MIC4Config()
    def setup(self, conifgID=50):
        self.mic4.connect()
>>>>>>> 2eac84198d3ff0a722ad9a728eb512bea29c1bde

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

def getdata(en1, fname, i=0, j=1, splitor=' ',k=None):
    lines = None
    with open(fname,'r') as fin:
        lines = fin.readlines()
    for line in lines:
        fs = line.rstrip().split(splitor)
#         print fs
        x = float(fs[i])
        if k: x -= float(fs[k])
#         print x, int(fs[j])
        en1.data1.push_back((x,int(fs[j])))
    print en1.data1.size()

def data2graph(data1, p1, fUnit=1):
    list1 = [0]*(p1.GetNbinsX()+2)
    for x in data1:
        ib = p1.Fill(x.first*fUnit,x.second)
        list1[ib]+=x.first*fUnit
    g1 = TGraphErrors()
    for i in range(p1.GetNbinsX()+2):
        N = p1.GetBinEntries(i)
        if N==0: continue

        n = g1.GetN()
        g1.SetPoint(n, list1[i]/N, p1.GetBinContent(i))
        g1.SetPointError(n, 0, p1.GetBinError(i))

    return g1

def plotResults(en1, info=None, savename='temp_fig/test'):
#     p1 = TProfile('h1','h1;#DeltaU [V];Prob',100,en1.mean-8*en1.sigma, en1.mean+8*en1.sigma)
    fUnit = 1000./0.7
    mean = en1.mean*fUnit
    sigma = en1.sigma*fUnit
    p1 = TProfile('h1','h1;N_{e^{-}};Prob',100,mean-8*sigma, mean+8*sigma)
    g1 = data2graph(en1.data1, p1, fUnit)
    p1.Draw('axis')

    fun1 = TF1('fun1',"0.5*(1+TMath::Erf((x-[0])/(TMath::Sqrt(2)*[1])))",0,1000)
    fun1.SetParameter(0,mean)
    fun1.SetParameter(1,sigma)
    fun1.SetLineColor(2)
    fun1.Draw('same')

    sUnit = 'e^{-}'
    lt = TLatex()
    lt.DrawLatexNDC(0.185,0.89,'#mu = {0:.1f} #pm {1:.1f} {2}'.format(en1.mean*fUnit, en1.meanErr*fUnit, sUnit))
    lt.DrawLatexNDC(0.185,0.84,'#sigma = {0:.1f} #pm {1:.1f} {2}'.format(en1.sigma*fUnit, en1.sigmaErr*fUnit, sUnit))

    if info:
        lt.DrawLatexNDC(0.185,0.75, info)

    print 'TMath::Gaus(x,{0:.5f},{1:.5f})'.format(mean, sigma)
    fun2 = TF1('gaus1','TMath::Gaus(x,{0:.5f},{1:.5f})'.format(mean, sigma),0,1000)
    fun2.SetLineColor(4)
    fun2.SetLineStyle(2)
    fun2.Draw('same')

    lg = TLegend(0.7,0.35, 0.95, 0.5)
    lg.SetFillStyle(0)
    lg.AddEntry(p1,'Measurement','p')
    lg.AddEntry(fun1,'Fit','l')
    lg.AddEntry(fun2,'Gaus','l')
    lg.Draw()

    g1.Draw("Psame")
    waitRootCmdX(savename)

def testFitter(fname, info=None, savename='figs_temp/test', mean0=0.5):
    en1 = encFitter()
<<<<<<< HEAD
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

#     en1.test("../data/dOut/ENC_0507_Chip5Col12_scan_normal_try1.dat")
#     en1.test(fname)
    getdata(en1, fname, 2, 4, k=1)
    en1.showData(10,3)
    en1.mean0 = mean0
    en1.fit()

    plotResults(en1,info, savename)

def test2():
    info = None
    savename = 'test1'
    en1 = encFitter()
    en1.data1.push_back((0.1,0))
    en1.data1.push_back((0.3,0))
    en1.data1.push_back((0.3,0))
    en1.data1.push_back((0.3,1))
    en1.data1.push_back((0.35,1))
    en1.data1.push_back((0.35,0))
    en1.data1.push_back((0.4,0))
    en1.data1.push_back((0.4,1))
    en1.data1.push_back((0.4,1))
    en1.data1.push_back((0.5,1))
   
    en1.mean0 = 0.35
    en1.sigma0 = 0.02
    en1.fit()
    print en1.mean, en1.sigma

    plotResults(en1)
    return


def test3():
    en1 = encFitter()
    getdata(en1, '/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan1.dat', 2, 4, k=1)
    getdata(en1, '/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan2_mod.dat', 2, 4, k=1)
    en1.mean0 = 0.155
    en1.fit()
    plotResults(en1,None, sDir+'norm1')


def test1(tag=''):
#     testFitter('../data/dOut/ENC_0507_Chip5Col12_scan_normal_try1.dat')
#     testFitter('../data/ENC/ENC_0508_Chip5Col12_scan_sub-3v_bias3.dat','sub-3v_bias3', sDir+tag+'sub_m3v_bias3',0.14)
#     testFitter('../data/ENC/ENC_0508_Chip5Col12_scan_sub-3v_bias5.dat','sub-3v_bias5', sDir+tag+'sub_m3v_bias5',0.14)
    testFitter('../data/ENC/ENC_0508_Chip5Col12_scan_sub-3v_bias6.dat','sub-3v_bias6', sDir+tag+'sub_m3v_bias6',0.1)

def test4():
    fun2 = TF1('gaus1','TMath::Gaus(x,{0:.5f},{1:.5f})'.format(mean, sigma))
    fun2.SetLineColor(4)
    fun2.SetLineStyle(2)
    fun2.Draw()

if __name__ == '__main__':
    useAtlasStyle()
    test1('Ne_')
#     test2()
#     test3()
#     testFitter()
=======
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
>>>>>>> 2eac84198d3ff0a722ad9a728eb512bea29c1bde
