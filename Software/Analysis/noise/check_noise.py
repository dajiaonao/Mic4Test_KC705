#!/usr/bin/env python
import sys
sys.path.append('../../Control/src')
from MIC4Config import getAddresses
from ROOT import TH2F, gStyle, TCanvas
from rootUtil import waitRootCmdX
from dateutil.parser import parse

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
#
    with open('test_data_out1.dat','r') as fin1:
        started = False
        date0 = parse('2018-05-11 21:52:35.0')
        date1 = parse('2018-05-11 22:52:35.0')
        while True:
            line = fin1.readline()
            if len(line)==0: break 
            if line[0:5]=='#2018':
                print line,
                date = parse(line[1:])
                print date
                started = date0<date<date1
            elif started:
                adds = getAddresses(line[:-1])
                if adds:
                    for x in adds:
#                         if x not in valid_list:
#                             print [ord(w) for w in line[:-1]] 
#                             print adds
#                             getAddresses(line[:-1],True)
#                             print x
#                             return 0
                        h2.Fill(x[1],x[0])
    h2.Draw('colzsame')
    waitRootCmdX()

if __name__ == '__main__':
    test()
