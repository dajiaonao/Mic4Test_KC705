#!/usr/bin/env python

from ROOT import TGraphErrors, gStyle
from rootUtil import waitRootCmdX, useAtlasStyle

def get_lines(fname):
    lines = None
    with open(fname,'r') as f1:
        lines = f1.readlines()
    return lines


lines = get_lines('DAC_scan_vreset_1p1TO1p3_save.dat')

gr1 = TGraphErrors()
gr2 = TGraphErrors()

fUnit = 1000./0.7
yUnit = 'e^{-}'

for line in lines:
    if len(line)==0: continue
    if line[0] in ['#','\n']: continue
    fs = line.rstrip().split()

    ix = int(fs[0])
    gr1.SetPoint(ix, float(fs[1]), float(fs[2])*fUnit)
    gr1.SetPointError(ix, 0, float(fs[3])*fUnit)
    gr2.SetPoint(ix, float(fs[1]), float(fs[4])*fUnit)
    gr2.SetPointError(ix, 0, float(fs[5])*fUnit)

useAtlasStyle()
gStyle.SetMarkerStyle(20)

gr1.Draw('AP')
h1 = gr1.GetHistogram()
h1.GetYaxis().SetTitle("Threshold ["+yUnit+"]")
h1.GetXaxis().SetTitle("V_{Reset} [V]")
# h1.GetYaxis().SetRangeUser(0,0.2)
waitRootCmdX()

gr2.Draw('AP')
h2 = gr2.GetHistogram()
h2.GetYaxis().SetTitle("ENC ["+yUnit+"]")
h2.GetXaxis().SetTitle("V_{Reset} [V]")
waitRootCmdX()
