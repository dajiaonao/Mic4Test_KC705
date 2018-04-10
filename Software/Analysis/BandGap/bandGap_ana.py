#!/usr/bin/env python
import os, sys, re
from math import sqrt
from ROOT import *
from rootUtil import useAtlasStyle, waitRootCmdX, savehistory, mkupHistSimple, get_default_fig_dir
funlist=[]

sDir = get_default_fig_dir()
sTag = 'test_'
sDirectly = False
if gROOT.IsBatch(): sDirectly = True

class dataSet1:
    def __init__(self, gr, mean, var2,yMin=None, yMax=None):
        self.gr = gr
        self.mean = mean
        self.var2 = var2
        self.yMin = yMin
        self.yMax = yMax

class VMeasure:
    y_scale = 1000.
    def __init__(self, fname=None):
        self.fname = fname
        self.lines = None
        self.y_shift = 0
        self.nP = None

        self.getInfo()
        pass
    def getInfo(self):
        if self.fname:
            with open(self.fname, 'r') as fin:
                self.lines = [x.rstrip() for x in fin.readlines()]

    def fillHist(self, idx0, h):
        idx = 0
        for l in self.lines:
            if len(l) == 0:
                if idx == idx0: break
                idx += 1
                continue
            if idx != idx0: continue

            if l[0] == '#': continue
            fs = l.split(',')
            h.Fill(float(fs[2])*self.y_scale + self.y_shift)

    def getGraph2(self, idxC=None, shifts=(0,0), shift=False):
        '''Take the data in idxC to make a TGraph, shift (t,y) by shifts'''
        g1 = TGraph()

        idx = 0
        sum1 = 0
        var2 = 0
        yMin = None
        yMax = None
        for l in self.lines:
            if len(l) == 0:
                idx += 1
                if inside: inside = False
                continue
            if idxC and idx not in idxC: continue
            inside = True

            if l[0] == '#': continue
            fs = l.split(',')
            y = float(fs[2])*self.y_scale - shifts[1]
            n = g1.GetN()
            g1.SetPoint(n, float(fs[1])-shifts[0], y)
            sum1 += y
            var2 += y*y
            if yMin is None or yMin>y: yMin = y
            if yMax is None or yMax<y: yMax = y

        n = g1.GetN()
        mean = sum1/n
        var2 = var2/n-mean*mean

        if shift:
            for i in range(n):
                x,y = Double(0), Double(0)
                g1.GetPoint(i,x,y)
                g1.SetPoint(i,x,y-mean)
            yMin -= mean
            yMax -= mean

        return dataSet1(g1, mean, var2, yMin, yMax)

    def getGraph(self, idx0=0, shift=False):
        g1 = TGraph()

        idx = 0
        sum1 = 0
        var2 = 0
        yMin = None
        yMax = None
        for l in self.lines:
            if len(l) == 0:
                if idx == idx0: break
                idx += 1
                continue
            if idx != idx0: continue

            if l[0] == '#': continue
            fs = l.split(',')
            y = float(fs[2])*self.y_scale + self.y_shift
            n = g1.GetN()
            g1.SetPoint(n, float(fs[1]), y)
            sum1 += y
            var2 += y*y
            if yMin is None or yMin>y: yMin = y
            if yMax is None or yMax<y: yMax = y

        n = g1.GetN()
        mean = sum1/n
        var2 = var2/n-mean*mean

        if shift:
            for i in range(n):
                x,y = Double(0), Double(0)
                g1.GetPoint(i,x,y)
                g1.SetPoint(i,x,y-mean)
            yMin -= mean
            yMax -= mean

        return dataSet1(g1, mean, var2, yMin, yMax)

    def getNP(self):
        self.nP = 0
        inside = False
        for l in self.lines:
            if len(l) == 0:
                if inside:
                    self.nP += 1
                    inside = False
                continue
            if l[0] == '#':
                inside = True
 
    def getAverageGraph(self,g1=None,nP=None,xshift=0):
        '''Check the avarge over time'''
        sft = False
        if g1 is None:
            g1 = TGraphErrors()
        if nP is None:
            if self.nP is None: self.getNP()
            nP = self.nP
        for idx0 in range(nP):
            r1 = self.getGraph(idx0, sft)
            g1.SetPoint(idx0, idx0+xshift, r1.mean)
            g1.SetPointError(idx0, 0, sqrt(r1.var2))
        return g1
     
def checkTD():
    '''Check the temperature dependence'''
    print "test"
    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/'
    vC1 = VMeasure(dir1+'BandGap_test1a/temprature_test_b3c1.dat')

    ### the the graph
    gr2 = vC1.getGraph(5)
    gr2.gr.Draw("APL")
    waitRootCmdX()



def test():
    checkLongScaleT()
#     checkTD()

def checkStability():
#     checkSample(4)
#     checkSample(9)
#     checkLongScale();
    checkHistos()
    return
    global sTag
    sTag = 'checkSample_'
    for i in range(10):
        checkSample(i)

def checkHistos():
    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/'
    sft = False
    VMeasure.y_scale = 1

    lg = TLegend(0.7,0.8,0.9,0.95)
    lg.SetFillStyle(0)

    h1 = TH1F("hS","hMeasV;Measured V [V];#Entries", 100,1.118,1.128)
    h2 = h1.Clone("hC1")
    h3 = h1.Clone("hC2")
    h2.SetLineColor(2)
    h2.SetMarkerColor(2)
    h2.SetMarkerStyle(24)
    h3.SetLineColor(4)
    h3.SetMarkerColor(4)
    h3.SetMarkerStyle(25)
    lg.AddEntry(h1,"V Source (shifted)",'pl')
    lg.AddEntry(h2,"Board 3, Chip 1",'pl')
    lg.AddEntry(h3,"Board 3, Chip 2",'pl')

    ms = VMeasure(dir1+'BandGap_test1a/source.dat')
    ms.y_shift = 0.12
    mC1 = VMeasure(dir1+'BandGap_test1a/b3c1.dat')
    mC2 = VMeasure(dir1+'BandGap_test1a/b3c2.dat')

    for idx0 in range(10):
        ms.fillHist(idx0, h1)
        mC1.fillHist(idx0, h2)
        mC2.fillHist(idx0, h3)

    print h1.GetEntries()
    h1.Draw("hist")
    h2.Draw("same")
    h3.Draw("same")

    lg.Draw()

    waitRootCmdX()


def checkLongScaleT():
    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/'
    sft = False
    VMeasure.y_scale = 1

    lg = TLegend(0.7,0.8,0.9,0.95)
    lg.SetFillStyle(0)

    g2 = TGraphErrors()
    g3 = TGraphErrors()
    g2.SetLineColor(2)
    g2.SetMarkerColor(2)
    g2.SetMarkerStyle(24)
    g3.SetLineColor(4)
    g3.SetMarkerColor(4)
    g3.SetMarkerStyle(25)
    lg.AddEntry(g2,"Board 3, Chip 1",'pl')
    lg.AddEntry(g3,"Board 3, Chip 2",'pl')

    mC1 = VMeasure(dir1+'BandGap_test1a/temprature_test_b3c1.dat')
    mC2 = VMeasure(dir1+'BandGap_test1a/temprature_test_b3c2.dat')

    mC1.getAverageGraph(g2)
    mC2.getAverageGraph(g3)

    g2.Draw("APL")
    g3.Draw("PL")
    h1 = g2.GetHistogram()

    lg.Draw()

    h1.GetYaxis().SetTitle("V [V]")
    h1.GetXaxis().SetTitle("t [min]")
    h1.GetYaxis().SetRangeUser(1.118,1.128)

    waitRootCmdX()



def checkLongScale():
    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/'
    sft = False
    VMeasure.y_scale = 1

    lg = TLegend(0.7,0.8,0.9,0.95)
    lg.SetFillStyle(0)

    g1 = TGraphErrors()
    g2 = TGraphErrors()
    g3 = TGraphErrors()
    g2.SetLineColor(2)
    g2.SetMarkerColor(2)
    g2.SetMarkerStyle(24)
    g3.SetLineColor(4)
    g3.SetMarkerColor(4)
    g3.SetMarkerStyle(25)
    lg.AddEntry(g1,"V Source",'pl')
    lg.AddEntry(g2,"Board 3, Chip 1",'pl')
    lg.AddEntry(g3,"Board 3, Chip 2",'pl')

    ms = VMeasure(dir1+'BandGap_test1a/source.dat')
    ms.y_shift = 0.12
    mC1 = VMeasure(dir1+'BandGap_test1a/b3c1.dat')
    mC2 = VMeasure(dir1+'BandGap_test1a/b3c2.dat')

    for idx0 in range(10):
        r1 = ms.getGraph (idx0, sft)
        r2 = mC1.getGraph(idx0, sft)
        r3 = mC2.getGraph(idx0, sft)

        g1.SetPoint(idx0, idx0+0.5, r1.mean)
        g1.SetPointError(idx0, 0, sqrt(r1.var2))
        g2.SetPoint(idx0, idx0+0.5, r2.mean)
        g2.SetPointError(idx0, 0, sqrt(r2.var2))
        g3.SetPoint(idx0, idx0+0.5, r3.mean)
        g3.SetPointError(idx0, 0, sqrt(r3.var2))

    g1.Draw("APL")
    g2.Draw("PL")
    g3.Draw("PL")
    h1 = g1.GetHistogram()

    lg.Draw()

    h1.GetYaxis().SetTitle("V [V]")
    h1.GetXaxis().SetTitle("Sample index")
#     h1.GetYaxis().SetRangeUser(0.9*min([p.yMin for p in [g1,g2,g3]]),1.1*max([p.yMax for p in [g1,g2,g3]]))
    h1.GetYaxis().SetRangeUser(1.118,1.128)

#     lt = TLatex()
#     lt.DrawLatexNDC(0.2,0.9,")

    waitRootCmdX()



def checkSample(idx0=4):
    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/'
    sft = True

    lg = TLegend(0.7,0.8,0.9,0.95)
    lg.SetFillStyle(0)

    ms = VMeasure(dir1+'BandGap_test1a/source.dat')
    g1 = ms.getGraph(idx0, sft)
    g1.gr.Draw('APL')
    h1 = g1.gr.GetHistogram()
    lg.AddEntry(g1.gr,"V Source",'pl')

    mC1 = VMeasure(dir1+'BandGap_test1a/b3c1.dat')
    g2 = mC1.getGraph(idx0, sft)
    g2.gr.SetLineColor(2)
    g2.gr.SetMarkerColor(2)
    g2.gr.SetMarkerStyle(24)
    g2.gr.Draw('PL')
    lg.AddEntry(g2.gr,"Board 3, Chip 1",'pl')

    mC2 = VMeasure(dir1+'BandGap_test1a/b3c2.dat')
    g3 = mC2.getGraph(idx0, sft)
    g3.gr.SetLineColor(4)
    g3.gr.SetMarkerColor(4)
    g3.gr.SetMarkerStyle(25)
    g3.gr.Draw('PL')
    lg.AddEntry(g3.gr,"Board 3, Chip 2",'pl')

    lg.Draw()

    h1.GetYaxis().SetTitle("#Delta V [mV]")
    h1.GetXaxis().SetTitle("t [s]")
    h1.GetYaxis().SetRangeUser(0.9*min([p.yMin for p in [g1,g2,g3]]+[-1]),1.1*max([p.yMax for p in [g1,g2,g3]]+[1]))
#     h1.GetYaxis().SetRangeUser(-1,1)

    lt = TLatex()
    lt.DrawLatexNDC(0.2,0.9,"Sample #{0:d}".format(idx0))

    waitRootCmdX(sDir+sTag+str(idx0))


def test1():
    dir0 = os.getenv('SAMPLEDIR_LAMB')
    print dir0

    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/'

    lines = None
    with open(dir1+'BandGap_test1a/b3c1.dat','r') as f1:
        lines = f1.readlines()
    idx0 = 3
    g1 = TGraph()

    idx = 0
    for l in lines:
        l = l.rstrip()
        if len(l) == 0:
            if idx == idx0: break
            idx += 1
            continue
        if idx != idx0: continue

        if l[0] == '#': continue
        print l
        fs = [float(x) for x in l.split(',')]
        n = g1.GetN()
        g1.SetPoint(n, fs[1], fs[2])

    g1.Draw("APL")

    waitRootCmd()
funlist.append(test)

if __name__ == '__main__':
    savehistory('.')
    useAtlasStyle()
    test()
#     for fun in funlist: print fun()
