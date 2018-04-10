#!/usr/bin/env python
from dateutil.parser import parse
import numpy as nm
from ROOT import TGraphErrors, TH2F, gStyle, TLegend
from rootUtil import waitRootCmdX

date = '2017-03-15 '
### A list of T

class Tsample:
    def __init__(self,T,times,name=None,data=[],date=None):
        self.name = name
        self.T = T
        self.times = times
        self.data = []
        self.date = date
        self.setTimes(self.times)

    def setTimes(self, times):
        date = '' if self.date is None else self.date+' '
        self.Times = [(parse(date+x[0]),parse(date+x[1])) for x in times]

def getGraph(Ts, filename):
    lines = None
    with open(filename) as f1:
        lines = f1.readlines()

    Tx = None
    for line in lines:
        ### find the associated tamperature
        line = line.rstrip()
        if len(line) == 0:
            Tx = None
            continue

        if line[0] == '#':
            fs = line.split()
            data = fs[1]+' '+fs[2]
            b = parse(data)
            if b is None: continue

            for x in Ts:
                for y in x.Times:
                    if b>y[0] and b<y[1]:
                        Tx = x
                        print b, Tx.T
                        break
                if Tx is not None: break
            continue

        if Tx is None: continue
        ### Add the samples to it
        fs = line.split(',')
        if len(fs)<3:
            continue
        Tx.data.append(float(fs[2]))

    gr1 = TGraphErrors()
    for t in Ts:

        if len(t.data)==0: continue
        ### calculate the mean and err
        ### Fill in the tgraph
        print t.T, len(t.data), nm.mean(t.data), nm.std(t.data)
        i = gr1.GetN()
        gr1.SetPoint(i, t.T, nm.mean(t.data))
        gr1.SetPointError(i, 0, nm.std(t.data))

    return gr1


# Ts.append((20, ('14:02', '14:08'), []))
date1 = '2018-02-03'
Ts1 = []
Ts1.append(Tsample(-20,[('14:10','14:17')],date=date1))
Ts1.append(Tsample(-10,[('14:25','14:32')],date=date1))
Ts1.append(Tsample(  0,[('14:40','14:47')],date=date1))
Ts1.append(Tsample( 10,[('14:55','15:02')],date=date1))
Ts1.append(Tsample( 20,[('15:10','15:17')],date=date1))
Ts1.append(Tsample( 30,[('15:25','15:32')],date=date1))
Ts1.append(Tsample( 40,[('15:40','15:47')],date=date1))
Ts1.append(Tsample( 50,[('15:55','16:02')],date=date1))
Ts1.append(Tsample( 60,[('16:10','16:17')],date=date1))
Ts1.append(Tsample( 70,[('16:25','16:32')],date=date1))
Ts1.append(Tsample( 80,[('16:40','16:47')],date=date1))

Ts2 = []
Ts2.append(Tsample(-30,[('18:17','18:24')],date=date1))
Ts2.append(Tsample(-20,[('18:32','18:39')],date=date1))
Ts2.append(Tsample(-10,[('18:47','18:54')],date=date1))
Ts2.append(Tsample(  0,[('19:02','19:09')],date=date1))
Ts2.append(Tsample( 10,[('19:17','19:24')],date=date1))
Ts2.append(Tsample( 20,[('19:32','19:39')],date=date1))
Ts2.append(Tsample( 30,[('19:47','19:54')],date=date1))
Ts2.append(Tsample( 40,[('20:02','20:09')],date=date1))
Ts2.append(Tsample( 50,[('20:17','20:24')],date=date1))
Ts2.append(Tsample( 60,[('20:32','20:39')],date=date1))
Ts2.append(Tsample( 70,[('20:47','20:54')],date=date1))
Ts2.append(Tsample( 80,[('21:02','21:09')],date=date1))


# for x in Ts:
#     for y in x.Times:
#         print y[0], y[1]

### for each sample, there is a date, and start line


### A temperature has a list of samples


### when parsing the data, for each sample, we find a T, and add the data to it. Then finally mesure the averge for the temperature
gr2 = getGraph(Ts2, '../data/BandGap_test1a/temprature_test_b3c2.dat') 
gr1 = getGraph(Ts1, '../data/BandGap_test1a/temprature_test_b3c1.dat') 

gr1.SetLineColor(2)
gr1.SetMarkerColor(2)
gr1.SetMarkerStyle(25)
gr2.SetLineColor(4)
gr2.SetMarkerColor(4)
gr2.SetMarkerStyle(24)

lg = TLegend(0.2, 0.8, 0.4, 0.9)
lg.SetFillStyle(0)
lg.SetBorderSize(0)
lg.AddEntry(gr1, "Chip #1",'lp')
lg.AddEntry(gr2, "Chip #2",'lp')


gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadBottomMargin(0.1)
h1 = TH2F('h2','h2;T [#circC];Output [V]',100,-35,85,100,1.116,1.13)
h1.Draw()
gr2.Draw('P')
gr1.Draw('P')
lg.Draw()

waitRootCmdX()
