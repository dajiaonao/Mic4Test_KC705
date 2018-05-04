#!/usr/bin/env python
from ROOT import TTree, TProfile, TF1, TLatex, TLegend, TGraphErrors
from rootUtil import waitRootCmdX, useAtlasStyle

def showDecay():
    tree1 = TTree()
    tree1.ReadFile('/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan1.dat','idX/i:vL/F:vH:A:D/i:R:W')
    tree1.ReadFile('/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan2_mod.dat')

#     p1 = TProfile('p1','p1;#DeltaU [V];Prob',50,0.12,0.2)
#     tree1.Draw("W:(vH-vL)>>p1","","profE")

    tree1.Draw("R:(vH-vL)>>p1","","")



#     fun1 = TF1('fun1','0.5*(1+TMath::Erf((x-[0])/(TMath::Sqrt(2)*[1])))',0.05,0.3)
#     fun1.SetParameter(0,0.155);
#     fun1.SetParameter(1,0.005);
# 
#     p1.Fit(fun1)
#     fun1a = p1.GetFunction('fun1')
#     fun1a.SetLineColor(2)
# 
#     p1.Draw("Esame")
# 
#     v0 = fun1a.GetParameter(0)
#     e0 = fun1a.GetParError(0)
#     v1 = fun1a.GetParameter(1)
#     e1 = fun1a.GetParError(1)
# 
#     print v0, v1
# 
#     fUnit = 1000.
#     lt = TLatex()
#     lt.DrawLatexNDC(0.185,0.89,'#mu = {0:.1f} #pm {1:.1f} mV'.format(v0*fUnit, e0*fUnit))
#     lt.DrawLatexNDC(0.185,0.84,'#sigma = {0:.1f} #pm {1:.1f} mV'.format(v1*fUnit, e1*fUnit))
# 
#     print 'TMath::Gaus(x,{0:.5f},{1:.5f})'.format(v0, v1)
#     fun2 = TF1('gaus1','TMath::Gaus(x,{0:.5f},{1:.5f})'.format(v0, v1))
#     fun2.SetLineColor(4)
#     fun2.SetLineStyle(2)
#     fun2.Draw('same')
# 
#     lg = TLegend(0.7,0.4, 0.95, 0.5)
#     lg.SetFillStyle(0)
#     lg.AddEntry(p1,'Measurement','p')
#     lg.AddEntry(fun1a,'Fit','l')
#     lg.AddEntry(fun2,'Gaus','l')
#     lg.Draw()

    waitRootCmdX()

def showENC():
    fname1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan1.dat'


    tree1 = TTree()
    tree1.ReadFile('/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan1.dat','idX/i:vL/F:vH:A:D/i:R:W')
    tree1.ReadFile('/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/ENC_Chip5Col12_scan2_mod.dat')

    tree1.Show(500)

    p1 = TProfile('p1','p1;#DeltaU [V];Prob',50,0.12,0.2)
    tree1.Draw("D:(vH-vL)>>p1","","profE")

    ### change it to tgraph
    g1 = TGraphErrors()
    for i in range(p1.GetNbinsX()+2):
        N = p1.GetBinEntries(i)
        if N>0:
            print i, N, p1.GetXaxis().GetBinCenter(i), p1.GetBinContent(i), p1.GetBinError(i)
            n = g1.GetN()
            g1.SetPoint(n, p1.GetXaxis().GetBinCenter(i), p1.GetBinContent(i))
            g1.SetPointError(n, 0, p1.GetBinError(i))
#     g1.SetMarkerColor(3)
#     g1.SetLineColor(3)


    p1.Draw("axis")
    g1.Draw('Psame')

    fun1 = TF1('fun1','0.5*(1+TMath::Erf((x-[0])/(TMath::Sqrt(2)*[1])))',0.05,0.3)
    fun1.SetParameter(0,0.155);
    fun1.SetParameter(1,0.005);

    g1.Fit(fun1)
    fun1a = g1.GetFunction('fun1')

#     p1.Fit(fun1)
#     fun1a = p1.GetFunction('fun1')
    fun1a.SetLineColor(2)

#     p1.Draw("Esame")

    v0 = fun1a.GetParameter(0)
    e0 = fun1a.GetParError(0)
    v1 = fun1a.GetParameter(1)
    e1 = fun1a.GetParError(1)

    print v0, v1

    fUnit = 1000.
    lt = TLatex()
    lt.DrawLatexNDC(0.185,0.89,'#mu = {0:.1f} #pm {1:.1f} mV'.format(v0*fUnit, e0*fUnit))
    lt.DrawLatexNDC(0.185,0.84,'#sigma = {0:.1f} #pm {1:.1f} mV'.format(v1*fUnit, e1*fUnit))

    print 'TMath::Gaus(x,{0:.5f},{1:.5f})'.format(v0, v1)
    fun2 = TF1('gaus1','TMath::Gaus(x,{0:.5f},{1:.5f})'.format(v0, v1))
    fun2.SetLineColor(4)
    fun2.SetLineStyle(2)
    fun2.Draw('same')

    lg = TLegend(0.7,0.4, 0.95, 0.5)
    lg.SetFillStyle(0)
    lg.AddEntry(p1,'Measurement','p')
    lg.AddEntry(fun1a,'Fit','l')
    lg.AddEntry(fun2,'Gaus','l')
    lg.Draw()

    waitRootCmdX()

class encChecker:
    def __init__(self):
        self.dataFiles = None
        self.bins = (50,0,1)
        pass
    def showENC(self):
        tree1 = TTree()
        header = 'idX/i:vL/F:vH:A:D/i:R:W'
        first = True
        for f in self.dataFiles:
            if first: tree1.ReadFile(f,header)
            else: tree1.ReadFile(f)

        p1 = TProfile('p1','p1;#DeltaU [V];Prob',self.bins[0],tree1.GetMinimum('vH-vL')*0.8,tree1.GetMaximum('vH-vL')*1.2)
        tree1.Draw("D:(vH-vL)>>p1","","profE")

        ### change it to tgraph
        g1 = TGraphErrors()
        for i in range(p1.GetNbinsX()+2):
            N = p1.GetBinEntries(i)
            if N>0:
                print i, N, p1.GetXaxis().GetBinCenter(i), p1.GetBinContent(i), p1.GetBinError(i)
                n = g1.GetN()
                g1.SetPoint(n, p1.GetXaxis().GetBinCenter(i), p1.GetBinContent(i))
                g1.SetPointError(n, 0, p1.GetBinError(i))

        p1.Draw("axis")
        g1.Draw('Psame')

        fun1 = TF1('fun1','0.5*(1+TMath::Erf((x-[0])/(TMath::Sqrt(2)*[1])))',0.05,0.3)
        fun1.SetParameter(0,0.155);
        fun1.SetParameter(1,0.005);

        g1.Fit(fun1)
        fun1a = g1.GetFunction('fun1')

        fun1a.SetLineColor(2)

        v0 = fun1a.GetParameter(0)
        e0 = fun1a.GetParError(0)
        v1 = fun1a.GetParameter(1)
        e1 = fun1a.GetParError(1)

        print v0, v1

        fUnit = 1000.
        lt = TLatex()
        lt.DrawLatexNDC(0.185,0.89,'#mu = {0:.1f} #pm {1:.1f} mV'.format(v0*fUnit, e0*fUnit))
        lt.DrawLatexNDC(0.185,0.84,'#sigma = {0:.1f} #pm {1:.1f} mV'.format(v1*fUnit, e1*fUnit))

        print 'TMath::Gaus(x,{0:.5f},{1:.5f})'.format(v0, v1)
        fun2 = TF1('gaus1','TMath::Gaus(x,{0:.5f},{1:.5f})'.format(v0, v1))
        fun2.SetLineColor(4)
        fun2.SetLineStyle(2)
        fun2.Draw('same')

        lg = TLegend(0.7,0.4, 0.95, 0.5)
        lg.SetFillStyle(0)
        lg.AddEntry(p1,'Measurement','p')
        lg.AddEntry(fun1a,'Fit','l')
        lg.AddEntry(fun2,'Gaus','l')
        lg.Draw()

        waitRootCmdX()


def test1A():
    dir1 = '/data/repos/Mic4Test_KC705/Software/Analysis/data/ENC/'
    enc1 = encChecker()
    enc1.dataFiles = [dir1+'ENC_0504_Chip5Col12_scan_sub-3v.dat']

    enc1.showENC()


if __name__ == '__main__':
    useAtlasStyle()
#     showENC()
    test1A()
#     showDecay()
