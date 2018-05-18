#!/usr/bin/env python
from ROOT import *

# gROOT.LoadMacro('encFitter.C+')
# from ROOT import encFitter

from run_ENC_scan import pixelData
from rootUtil import waitRootCmdX, useAtlasStyle


def test1():
    p1 = pixelData((120,29))
#     p1.loadFromFile('/data/repos/Mic4Test_KC705/Software/Analysis/ENC/May18_enc_scan_BlockRow15.dat', lambda x: 0.019<x<0.06667)
#     p1.loadFromFile('/data/repos/Mic4Test_KC705/Software/Analysis/ENC/May18_enc_scan_BlockRow15.dat', lambda x:0.05<x<0.15)
    p1.loadFromFile('/data/repos/Mic4Test_KC705/Software/Analysis/ENC/May18_enc_scan_BlockRow15.dat')
    p1.ENC()

    gr1 = p1.getGraph()
    gr1.Draw('AP')

    fun1 = p1.getFitFun()
    fun1.Draw('same')
    fun1.SetLineColor(2)
    print p1.getFitChi2()
    waitRootCmdX()

if __name__ == '__main__':
    useAtlasStyle()
    test1()
