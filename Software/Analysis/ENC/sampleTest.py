#!/usr/bin/env python
import random, math
from ROOT import TH1F, TGraph, TCanvas
from rootUtil import waitRootCmdX, useAtlasStyle

class xBin:
    def __init__(self,Range=None, totalY=0.01):
        self.Range = Range
        self.totalY = totalY
        self.Nevent = 0
    def contains(self,x):
        return self.Range[0] < x < self.Range[1]
    def next(self):
        a = self.Range[0]
        b = self.Range[1]
        print a, b
        print '->', random.random()
        return random.uniform(a,b)
#         return random.uniform(self.Range[0], self.Range[1])
    def center(self):
        return 0.5*(self.Range[0]+self.Range[1])
    def actualP(self):
        return self.totalY/(1+self.Nevent)
    def merge(self,b):
        self.Range = (min(self.Range[0], b.Range[0]), max(self.Range[1], b.Range[1]))
        self.Nevent += b.Nevent
        self.totalY += b.totalY
    def split(self):
        b1 = xBin(Range=(self.Range[0], self.center()))
        b1.Nevent = 0.5*self.Nevent
        b1.totalY = 0.5*self.totalY

        self.Range = (self.center(), self.Range[1])
        self.Nevent = b1.Nevent
        self.totalY = b1.totalY
        return b1


class sampler:
    def __init__(self,xRange=None, xNbins=None):
        self.xNbins = xNbins
        self.xRange = xRange
        self.xBins = None
        self.funX = None
        self.funY = None
        self.totalN = 0
        self.sFactor = 3.

        if self.xRange and self.xNbins:
            self.setup()
        
    def setup(self):
        v = 1./self.xNbins
        self.xBins = [xBin((v*i,v*(i+1)),v) for i in range(self.xNbins)]

    def findBin(self, x):
#         return next(b for b in self.xBins if b.contains(x)) if self.xRange[0] < x < self.xRange[1] else None
        return next((i, self.xBins[i]) for i in range(len(self.xBins)) if self.xBins[i].contains(x)) if self.xRange[0] < x < self.xRange[1] else None
    def getPDF(self,x):
        return self.funY(self.findBin(x).actualP)
    def next(self):
        return self.xBins[random.randint(0,len(self.xBins)-1)].next()
    def totalP(self):
        return sum([a.actualP() for a in self.xBins])
    def generate(self):
        x1 = self.next()
        y1 = self.funX(x1)
        self.totalN += 1
        print 'xxx->',x1
        ib,b = self.findBin(x1)
        b.Nevent += 1
#         b.totalY += self.funY(y1)/self.xNbins
        b.totalY += self.funY(y1)*self.sFactor/self.xNbins

        totalP = sum([a.actualP() for a in self.xBins])
        if b.actualP()>totalP/len(self.xBins):
            b1 = b.split()
            self.xBins.insert(ib, b1)
            self.rebin()
        return x1

    def rebin(self):
        minI, minV = min(enumerate([self.xBins[i].actualP()+self.xBins[i+1].actualP()] for i in range(self.xNbins-1)), key=lambda p:p[1])
        ### merge and delete
        self.xBins[minI+1].merge(self.xBins[minI])
        del self.xBins[minI]
    def show(self):
        i = 0
        totalP = 0
        for x in self.xBins:
            print i, x.Range, x.Nevent, x.totalY, x.actualP()
            totalP += x.actualP()
            i += 1
        print totalP

def test():
    s1 = sampler((0.,1.),100)
    s1.funX = lambda x:0.5*(1+math.erf((x-0.4)/0.04))
    s1.funY = lambda x:x*(1.-x)/6.
    for i in range(10): print s1.funY(0.1*i)
    print s1.next()

    s1.sFactor = 80

    NEVT = 2000
    h1 = TH1F('h1','h1;x;Events',100,0,1)
#     h1 = TH1F('h1','h1;x;Events',NEVT,0,NEVT)
    g1 = TGraph()
    for i in range(NEVT):
#         h1.Fill(s1.next())
        h1.Fill(s1.generate())
#         h1.Fill(s1.totalP())
        g1.SetPoint(i,i,s1.totalP())
    s1.show()


    c1 = TCanvas()
    c1.Divide(2)
    c1.cd(1)
    h1.Draw()
    c1.cd(2)
    g1.Draw('AP')
    c1.cd()

    waitRootCmdX()

if __name__ == '__main__':
    useAtlasStyle()
    test()