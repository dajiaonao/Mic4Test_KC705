#!/usr/bin/env python
import sys
sys.path.append('../../Control/src')
from MIC4Config import getAddresses, getAddressesN
from ROOT import TH2F, gStyle, TCanvas, TLatex
from rootUtil import waitRootCmdX, bcolors
from dateutil.parser import parse


sDir = 'xray_figs/'
sTag = 'Jul27a_'
autoSave = False
# autoSave = True
bc1 = bcolors()

def setStyle():
    gStyle.SetOptStat(0)
    gStyle.SetPadRightMargin(0.18)
    gStyle.SetPadLeftMargin(0.15)
    gStyle.SetPadBottomMargin(0.1)
    gStyle.SetPadTopMargin(0.06)
    gStyle.SetOptTitle(0)
    gStyle.SetPalette(55)

def test():
    setStyle()
    h2 = TH2F('h2','h2;Col;Row',64,-0.5,63.5,128,-0.5,127.5)
    h2C = h2.Clone('h2C')
    valid_list = [(i+32*k,j,0,1) for i in range(7) for j in range(32) for k in range(4)]
    for t in [(i+32*k,j,0,1) for i in range(7) for j in range(32) for k in range(4)]:
        h2C.Fill(t[1],t[0])

    cav1 = TCanvas('cav1','cav1',400,700)
    h2C.Draw('box')
#     waitRootCmdX()
    lt = TLatex()
#
    figI = 0
    with open('../data/xRay/data_xRayTest_Jul27_1.dat','r') as fin1:
        started = False
        date0 = parse('2018-07-27 16:05:33.9')
        date1 = parse('2018-09-11 22:52:35.0')
#         datax = None
        datax = []
        while True:
            line = fin1.readline()
            if len(line)==0: break 
            if line[0:5]=='#2018':
#                 print line,
                date = parse(line[1:])
#                 print date
                started = date0<date<date1
            elif started:
#                 print [ord(w) for w in line]
                if datax: 
                    print '-->',datax
                    print '===',[ord(w) for w in line[:-1]]
                datax += [ord(w) for w in line[:-1]]
                adds,r = getAddressesN(datax, False)
                if r: 
                    print '>>>>',datax
                    print '++++',r
                if adds == [] or adds is None:
                    print '---:', date
                    print datax
                    print
                datax = r
                continue
                bc1.show("OKBLUE",str(date))
#                 print date
                print adds

                htx = h2.Clone('htx')
                if adds:
                    for x in adds:
#                         if x not in valid_list:
#                             print [ord(w) for w in line[:-1]] 
#                             print adds
#                             getAddresses(line[:-1],True)
#                             print x
#                             return 0
#                         h2.Fill(x[1],x[0])
                        htx.Fill(x[1],x[0])
                htx.Draw("colz")
                lt.DrawLatexNDC(0.2,0.95,str(date))
                waitRootCmdX(sDir+sTag+str(figI), autoSave)
                figI += 1

    h2.Draw('colzsame')
    waitRootCmdX()

if __name__ == '__main__':
    test()
