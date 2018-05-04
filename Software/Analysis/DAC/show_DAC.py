#!/usr/bin/env python
import numpy as nm
from ROOT import TGraphErrors, TGraph, TCanvas, gStyle, TLine, TLatex
from rootUtil import waitRootCmdX, useAtlasStyle, get_default_fig_dir

### Voltage and current DAC list
VList = [('VREF_Current_DAC','VRef'),('VCASN2','VCASN2'),('VReset','VReset'),('VCASP','VCASP'),('VCASN','VCASN'),('VCLIP','VCLIP')]
IList = [('IBIAS_IHEP_40n','IBIAS'),('IHEP_IFOL_2n','ITHR'),('IHEP_IRESET_40p','IRESET'),('IHEP_IDB2','IDB2'),('IBIAS','IBIAS'),('ITHR','ITHR'),('IDB','IDB')]


def showDAC(fname, Infox=None, saveName='temp_figs/test'):

    lines = None
    with open(fname,'r') as f1:
        lines = f1.readlines()

    gr1 = TGraphErrors()
    gr2 = TGraph()
    gr3 = TGraph()
    gr4 = TGraph()

    largeError = -1
    largeErrorI = None
    largeErrorMS = None

    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            continue
        elif line[0] == '#':
            fs = line.split()
            code = int(fs[3][5:], 16)
            print code
        else:
            ms = [float(x) for x in line.split(',')][1::2]
            mean = nm.mean(ms) 
            error = nm.std(ms)

            if error>largeError:
                largeError = error
                largeErrorI = code
                largeErrorMS = ms

            gr1.SetPoint(code, code, mean)
            gr1.SetPointError(code, 0, error)

    print largeErrorI, largeErrorMS, nm.mean(largeErrorMS), nm.mean(ms)
    for i in range(len(largeErrorMS)):
        gr4.SetPoint(i,i,largeErrorMS[i])


    N = gr1.GetN()
    Ys = gr1.GetY()
    print Ys[0], Ys[N-1], Ys[largeErrorI]
    LSB = (Ys[N-1]-Ys[0])/(N-1)
    print LSB
    for i in range(N):
        gr2.SetPoint(i, i, Ys[i]-(Ys[0]+i*LSB))
        gr3.SetPoint(i, i, Ys[i]-Ys[i-1] if i>0 else 0)


    line = TLine()
    lt = TLatex()

    cav1 = TCanvas('cav1','cav1',1000,800)
    cav1.Divide(2,2)
    cav1.cd(1)
    gr1.Draw('AP')
    h1 = gr1.GetHistogram()
    h1.GetXaxis().SetTitle('Code')
    h1.GetYaxis().SetTitle('U [V]')
    ln1 = line.DrawLine(0, Ys[0], N-1, Ys[N-1])
    ln1.SetLineColor(2)

    rgInfo = '[{0:.2g},{1:.2g}] V'.format(Ys[0],Ys[N-1])
    if Infox:
        rgInfo = Infox+': '+rgInfo
    lt.DrawLatexNDC(0.2, 0.85, rgInfo)


    cav1.cd(2)
    gr4.SetMarkerStyle(20)
    gr4.Draw('AP')
    h4 = gr4.GetHistogram()
    h4.GetXaxis().SetTitle('#it{i}th')
    h4.GetYaxis().SetTitle('U [V]')
    lt.DrawLatexNDC(0.2,0.85,"{0:d} measurements for code={1:d}".format(len(largeErrorMS), largeErrorI))

    cav1.cd(3)
    gr2.SetFillColor(2)
    gr2.Draw('APB')
    h2 = gr2.GetHistogram()
    h2.GetXaxis().SetTitle('Code')
    h2.GetYaxis().SetTitle('INL [V]')

    lY = LSB if gr2.GetMean(2)>0 else -LSB
    ln2 = line.DrawLine(0, lY, N, lY)
    ln2.SetLineStyle(2)

    lt.DrawLatexNDC(0.6,0.85, "Max INL={0:.1f} LSB".format(max([abs(x) for x in gr2.GetY()])/LSB))

    cav1.cd(4)
    gr3.SetFillColor(4)
    gr3.Draw('APB')
    h3 = gr3.GetHistogram()
    h3.GetXaxis().SetTitle('Code')
    h3.GetYaxis().SetTitle('DNL [V]')

    lY = LSB if gr3.GetMean(2)>0 else -LSB
    ln3 = line.DrawLine(0, lY, N, lY)
    ln3.SetLineStyle(2)
    lt.DrawLatexNDC(0.6,0.85, "Max DNL={0:.1f} LSB".format(max([abs(x) for x in gr3.GetY()])/LSB))

    cav1.cd()
    waitRootCmdX(saveName)


def easyCheck(idx):
    idy = idx%10
    xList = VList if idx<10 else IList

    dir1 = '../data/DAC/'
    dir2 = get_default_fig_dir()
    showDAC(dir1+'DAC_chip5_scan{0:d}.dat'.format(idx), xList[idy][0], dir2+xList[idy][0])

def runChecks():
#     for i in range(6): 
#         if i>1: break
#         if i!=2: continue
#         easyCheck(i)
    for i in range(10,17):
        easyCheck(i)

def test1():
    dir1 = '../data/DAC/'
    dir2 = get_default_fig_dir()
#     showDAC(dir1+'DAC_chip5_scan10.dat', IList[0][1])
    showDAC(dir1+'DAC_chip5_scan0.dat', VList[0][1], dir2+VList[0][1])
 

if __name__ == '__main__':
    useAtlasStyle()
    gStyle.SetMarkerStyle(1)
    gStyle.SetEndErrorSize(2)
    runChecks()
#     test1()
