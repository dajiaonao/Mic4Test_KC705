#!/usr/bin/env python
from ROOT import *

# gROOT.LoadMacro('encFitter.C+')
# from ROOT import encFitter
import math
from run_ENC_scan import pixelData
from rootUtil import waitRootCmdX, useAtlasStyle, savehistory

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
    test3()
