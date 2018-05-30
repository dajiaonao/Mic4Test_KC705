#!/usr/bin/env python
from ROOT import *

# gROOT.LoadMacro('encFitter.C+')
# from ROOT import encFitter
from collections import defaultdict
import math
from run_ENC_scan import pixelData
from rootUtil import waitRootCmdX, useAtlasStyle, savehistory


class ENC_stats():
    def __init__(self):
        h2temp = TH2F('htemp','Threshold;Col;Row',64,-0.5,63.5,128,-0.5,127.5)
        self.hgrid = h2temp.Clone('hgrid')
        self.hgrid.SetLineColor(4)
        self.hgrid.SetLineWidth(1)
        for x,y in [(x,y) for x in range(64) for y in range(128) if (x,y)!=(0,0)]: hgrid.Fill(x,y)

        self.h2_thr = h2temp.Clone('h_threshold') 
        self.h2_enc = h2temp.Clone('h_enc') 

        self.h1_thr = TH1F('h1_thr','h1_thr;#DeltaU [V];# Pixel',50,0,0.3)
        self.h1_enc = TH1F('h1_enc','h1_enc;#DeltaU [V];# Pixel',50,0,0.01)
        self.h1b_thr = h1_thr.Clone('h1b_thr')

        self.th2 = TH2F('th2','th2;#DeltaU [V];Prob',100,0,0.3,100,0,1)

    def show(self):
#         self.th2.Draw('axis')
# 
#         waitRootCmdX()

        tx1 = ''
        gPad.SetRightMargin(0.16)
    #     hgrid.Draw('box')
        self.h2_thr.Draw(tx1+'colz')
        waitRootCmdX()

    #     hgrid.Draw('box')
        self.h2_enc.Draw(tx1+'colz')
        waitRootCmdX()

        self.h1_thr.Draw()
        self.h1b_thr.SetLineColor(4)
        self.h1b_thr.Draw('same')
        lgT = TLegend(0.7,0.8,0.92,0.92)
        lgT.SetFillStyle(0)
        lgT.SetHeader("Threshold")
        lgT.AddEntry(h1_thr,"Last block row")
        lgT.AddEntry(h1b_thr,"Last pixel row")
        lgT.Draw()
        waitRootCmdX()

        self.h1_enc.Draw()
        waitRootCmdX()


class ENC_checkX():
    '''Take a file and process all the pxiels inside it'''
    def __init__(self, fname, stats=None):
        self.fname = fname
        self.corrTable = {}
        self.pixelList = None
        self.pixelData = {}
        self.stats = stats
        pass
    def loadFile(self):
        pX = lambda x,y: x if x>0 else y

        with open(self.fname,'r') as fin1:
            pxd = None
            while True:
                line = fin1.readline()
                if len(line)==0: break
                if line == '#---\n':
                    continue
                fs = line.rstrip().split()
                if len(fs)==0:
                    if pxd: pxd = None
                    continue

                if line[0]!='#' and len(fs)==6:
                    px = (int(fs[0]), int(fs[1]))
                    pxd = pixelData(px)
                    if fs[2] != '-1': pxd.mean = float(fs[2])
                    if fs[3] != '-1': pxd.meanErr = float(fs[3])
                    if fs[4] != '-1': pxd.sigma = float(fs[4])
                    if fs[5] != '-1': pxd.sigmaErr = float(fs[5])
                    self.pixelData[px] = pxd
                        
                if (pxd is not None) and fs[0]=='#':
                    x = float(fs[1])
                    pxd.totalStats[x] = int(fs[2])
                    pxd.passStats[x] = int(fs[3])

    def getCorrTable(self):
        self.lowX = 99.
        self.corrTable = defaultdict(int) 
        for px in self.pixelData.values():
            for x in px.totalStats.keys():
                if px.passStats[x] > self.corrTable[x]: self.corrTable[x] = px.passStats[x]
                if x < self.lowX and px.totalStats[x]>10 and float(px.passStats[x])/px.totalStats[x]>0.95: self.lowX = x

    def applyCorrection(self,px):
        for x in px.totalStats.keys():
            if x>self.lowX: px.totalStats[x] = self.corrTable[x]

    def showPix(self,p=None):
        p1 = p
        if p is None:
            dlist = [x.addr for x in self.pixelData.values()]
            print 'Avaliable pixels:', dlist

            if len(dlist)>0: p1 = dlist[0]
        if p1 is not None:
            try:
                print self.pixelData[p1].dumpInfo()
            except KeyError as e:
                print 'pixel', p1, 'is not found'

    def processAll(self,drawFit=True):
        if self.stats is None:
            self.stats = ENC_stats()
            if drawFit: self.stats.th2.Draw('axis')

        ci = 0
        for p1 in self.pixelData.values():
            r,c = p1.addr
            print '-'*10,p1.addr,'-'*10

            self.applyCorrection(p1)
            p1.dropIllData()
            p1.ENC()

            fun1 = p1.getFitFun()
            if drawFit: fun1.Draw('same')
            fun1.SetLineColor(TColor.GetColorPalette(ci))
            print p1.getFitChi2()

            self.stats.h2_thr.Fill(c,r,fun1.GetParameter(0))
            self.stats.h2_enc.Fill(c,r,fun1.GetParameter(1))

            self.stats.h1_thr.Fill(fun1.GetParameter(0))
            self.stats.h1_enc.Fill(fun1.GetParameter(1))

            if r==127:
                self.stats.h1b_thr.Fill(fun1.GetParameter(0))
            ci += 1
    def showCorrTable(self):
        for dv in sorted(self.corrTable.iterkeys()):
            print dv,self.corrTable[dv], dv>self.lowX

def test5():
    dir1 = '../data/'
    ex1 = ENC_checkX(dir1+'ENC/May30_Chip7_enc_scan_row72To79_col0To32.dat')
    ex1.loadFile()
    ex1.showPix()
    ex1.getCorrTable()
#     ex1.showCorrTable()
#     ex1.processAll()

    stats1 = ex1.stats
    ex2 = ENC_checkX(dir1+'ENC/May29_Chip7_enc_scan_row16To23_col0To32.dat',stats1)
    ex2.loadFile()
    ex2.getCorrTable()
#     ex2.processAll()

    pix = (21,21)
    ex2.showPix(pix)
    ex2.showCorrTable()
    ex2.applyCorrection(ex2.pixelData[pix])
    ex2.showPix(pix)
    ex2.pixelData[pix].dropIllData()
    ex2.showPix(pix)
    return

    if gPad : waitRootCmdX()
    stats1.show()

    return

    x1 = ex1.pixelData.values()[20]
    ex1.applyCorrection(x1)
    ex1.showPix()
    

    x1.ENC()
    x1.getGraph().Draw('APsame')
    fun1 = x1.getFitFun()
    fun1.SetLineColor(TColor.GetColorPalette(8))
    fun1.Draw('same')
    waitRootCmdX()

    


def test3():
    th2 = TH2F('th2','th2;#DeltaU [V];Prob',100,0,0.3,100,0,1)
    th2.Draw('axis')
    plist = []
    threshold = [0]*32
    for i in range(7,8):
        for j in range(32):
            r = 120+i
            c = j
            p1 = pixelData((r,c))
            p1.loadFromFile('May18_enc_scan_BlockRow15.dat')
            p1.ENC()

            p1.getGraph().Draw('Psame')

            fun1 = p1.getFitFun()
            fun1.Draw('same')
            fun1.SetLineColor(TColor.GetColorPalette(j*8))
            print p1.getFitChi2()
            plist.append(p1)
            threshold[j] = fun1.GetParameter(0)

    for i in range(len(threshold)):
        print i, threshold[i]
    

    waitRootCmdX()


def test2():
    h2temp = TH2F('htemp','Threshold;Col;Row',64,-0.5,63.5,128,-0.5,127.5)
    hgrid = h2temp.Clone('hgrid')
    hgrid.SetLineColor(4)
    hgrid.SetLineWidth(1)
    for x,y in [(x,y) for x in range(64) for y in range(128) if (x,y)!=(0,0)]: hgrid.Fill(x,y)
#     hgrid.Draw('box')
    print hgrid.GetEntries()

    
#     waitRootCmdX()
    h2_thr = h2temp.Clone('h_threshold') 
    h2_enc = h2temp.Clone('h_enc') 

    h1_thr = TH1F('h1_thr','h1_thr;#DeltaU [V];# Pixel',50,0,0.3)
    h1_enc = TH1F('h1_enc','h1_enc;#DeltaU [V];# Pixel',50,0,0.01)
    h1b_thr = h1_thr.Clone('h1b_thr')

    th2 = TH2F('th2','th2;#DeltaU [V];Prob',100,0,0.3,100,0,1)
    th2.Draw('axis')
    for i in range(8):
        for j in range(32):
            r = 120+i
            c = j
            p1 = pixelData((r,c))
            p1.loadFromFile('May18_enc_scan_BlockRow15.dat')
            p1.ENC()

            fun1 = p1.getFitFun()
            fun1.Draw('same')
            fun1.SetLineColor(TColor.GetColorPalette(i*32+j))
            print p1.getFitChi2()

            h2_thr.Fill(c,r,fun1.GetParameter(0))
            h2_enc.Fill(c,r,fun1.GetParameter(1))

            h1_thr.Fill(fun1.GetParameter(0))
            h1_enc.Fill(fun1.GetParameter(1))

            if r==127:
                h1b_thr.Fill(fun1.GetParameter(0))
    waitRootCmdX()

    tx1 = ''
    gPad.SetRightMargin(0.16)
#     hgrid.Draw('box')
    h2_thr.Draw(tx1+'colz')
    waitRootCmdX()

#     hgrid.Draw('box')
    h2_enc.Draw(tx1+'colz')
    waitRootCmdX()

    h1_thr.Draw()
    h1b_thr.SetLineColor(4)
    h1b_thr.Draw('same')
    lgT = TLegend(0.7,0.8,0.92,0.92)
    lgT.SetFillStyle(0)
    lgT.SetHeader("Threshold")
    lgT.AddEntry(h1_thr,"Last block row")
    lgT.AddEntry(h1b_thr,"Last pixel row")
    lgT.Draw()
    waitRootCmdX()

    h1_enc.Draw()
    waitRootCmdX()


def test1():
    p1 = pixelData((124,26))
#     p1.loadFromFile('/data/repos/Mic4Test_KC705/Software/Analysis/ENC/May18_enc_scan_BlockRow15.dat', lambda x: 0.019<x<0.06667)
#     p1.loadFromFile('/data/repos/Mic4Test_KC705/Software/Analysis/ENC/May18_enc_scan_BlockRow15.dat', lambda x:0.05<x<0.15)
    p1.loadFromFile('May18_enc_scan_BlockRow15.dat')
    p1.ENC()

    gr1 = p1.getGraph()
    gr1.Draw('AP')

    fun1 = p1.getFitFun(tryRecover=False)
    if math.isnan(p1.fitter.mean):
        fun1.SetParameter(0, p1.fitter.mean0)
        fun1.SetParameter(1, p1.fitter.sigma0)
        gr1.Fit(fun1)

    fun1.Draw('same')
    fun1.SetLineColor(2)
    print p1.getFitChi2()
    waitRootCmdX()

if __name__ == '__main__':
    useAtlasStyle()
    savehistory('./')
#     test2()
    test5()
