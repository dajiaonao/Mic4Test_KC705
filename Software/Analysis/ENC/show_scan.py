#!/usr/bin/env python

from ROOT import TGraphErrors, gStyle, TGaxis, gPad
from rootUtil import waitRootCmdX, useAtlasStyle
from array import array

def get_lines(fname):
    lines = None
    with open(fname,'r') as f1:
        lines = f1.readlines()
    return lines



def testIthr():
    lines = get_lines('DAC_scan_ithr_0x40to0xf0.dat')

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

    gr1.SetMarkerStyle(20)
    gr1.Draw('AP')
    h1 = gr1.GetHistogram()
    h1.GetYaxis().SetTitle("Threshold ["+yUnit+"]")
    h1.GetXaxis().SetTitle("I_{Thre} code")
    # h1.GetYaxis().SetRangeUser(0,0.2)

    gPad.SetTicks(1,0)
    gPad.SetRightMargin(0.16)

    y1b = 0
    y2b  = 15
    x1 = h1.GetXaxis().GetXmax()
    y1 = h1.GetYaxis().GetXmin()
    y2 = h1.GetYaxis().GetXmax()
    raxis = TGaxis(x1,y1,x1,y2,y1b,y2b,506,"+L");
    raxis.SetLineColor(2)
    raxis.SetLabelColor(2)
    raxis.SetTitleColor(2)
    raxis.SetTitle("ENC ["+yUnit+"]")
    raxis.Draw();

    nP = gr2.GetN()
    Ys = gr2.GetY()
    EYs = gr2.GetEY()
    Y = array('d',[y1+(y2-y1)/(y2b-y1b)*(Ys[i]-y1b) for i in range(nP)])
    EY = array('d',[(y2-y1)/(y2b-y1b)*EYs[i] for i in range(nP)])
    gr2x = TGraphErrors(nP, gr2.GetX(), Y, gr2.GetEX(), EY)
    gr2x.SetMarkerStyle(24)
    gr2x.SetLineColor(2)
    gr2x.SetMarkerColor(2)

    gr2x.Draw('Psame')

    waitRootCmdX()


def testVrest():
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

    gr1.SetMarkerStyle(20)
    gr1.Draw('AP')
    h1 = gr1.GetHistogram()
    h1.GetYaxis().SetTitle("Threshold ["+yUnit+"]")
    h1.GetXaxis().SetTitle("V_{Reset} [V]")
    # h1.GetYaxis().SetRangeUser(0,0.2)

    gPad.SetTicks(1,0)
    gPad.SetRightMargin(0.16)

    y1b = 0
    y2b  = 15
    x1 = h1.GetXaxis().GetXmax()
    y1 = h1.GetYaxis().GetXmin()
    y2 = h1.GetYaxis().GetXmax()
    raxis = TGaxis(x1,y1,x1,y2,y1b,y2b,506,"+L");
    raxis.SetLineColor(2)
    raxis.SetLabelColor(2)
    raxis.SetTitleColor(2)
    raxis.SetTitle("ENC ["+yUnit+"]")
    raxis.Draw();

    nP = gr2.GetN()
    Ys = gr2.GetY()
    EYs = gr2.GetEY()
    Y = array('d',[y1+(y2-y1)/(y2b-y1b)*(Ys[i]-y1b) for i in range(nP)])
    EY = array('d',[(y2-y1)/(y2b-y1b)*EYs[i] for i in range(nP)])
    gr2x = TGraphErrors(nP, gr2.GetX(), Y, gr2.GetEX(), EY)
    gr2x.SetMarkerStyle(24)
    gr2x.SetLineColor(2)
    gr2x.SetMarkerColor(2)

    gr2x.Draw('Psame')

    waitRootCmdX()

    gr2.Draw('AP')
    h2 = gr2.GetHistogram()
    h2.GetYaxis().SetTitle("ENC ["+yUnit+"]")
    h2.GetXaxis().SetTitle("V_{Reset} [V]")
    waitRootCmdX()

if __name__ == '__main__':
    testIthr()
