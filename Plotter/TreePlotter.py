from PlotterTools import *
from ROOT import *
import optparse
import argparse
from array import array
from MyCMSStyle import *
gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetOptFit()

parser = argparse.ArgumentParser(description='Plotter')

parser.add_argument('--Run', metavar='Run', type=str, nargs = '+', help='Run Number',required=True)
args = parser.parse_args()

ch = TChain('pulse')
for run in range(len(args.Run)):
    ch.Add(str(args.Run[run]))

for var in Vars:
    hist = var[1]
    h = TH1F(hist, var[2], var[3], var[4], var[5])
    tempCut = TCut(Cut)
    if "amp" in var[0]:
        Cut = var[0]+">100"
    ch.Draw(var[0]+'>>'+hist, TCut(Cut))
    h.SetLineColor(kBlack)
    h.SetLineWidth(2)
    h.GetYaxis().SetTitleOffset(1.5)

    c = TCanvas('c', 'c', 800, 600)
    h.Draw()
    c.SaveAs("Var_"+str(var[1])+".pdf")

    if doLanFit and "amp" in var[0]: ##--Landau fit of amplitude distribution
        fitResultPtr_lan = h.Fit("landau","S")
        chi2_nparams_lan = (fitResultPtr_lan.Chi2(), fitResultPtr_lan.NFreeParameters())
        c.Draw()
        c.SaveAs(outputLoc+"fitLan_"+str(var[1])+".pdf")

for chan in channel:
    graphs = TMultiGraph()
    leg = TLegend(0.6, 0.7, 0.89, 0.89)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.02)
    leg.SetFillColor(kWhite)
    for sen in range(len(sensor)):
        y =[]
        y_err = []
        x = cfdFrac
        x_err = [0,0,0,0,0,0,0,0,0,0]
        for f in cfdFrac:
            hist2 = "Ch"+str(chan)+"_"+str(f)
            h2 = TH1F(hist2,"Time Resolution; #Delta T CH"+str(chan)+"_"+str(f)+";Yields" , 100, 5e-09, 6e-09)
            ch.Draw("LP2_"+str(f)+"["+str(chan)+"]"+"-LP2_50[3]"+'>>'+hist2)
            c1 = TCanvas('c1', 'c1', 800, 600)
            GausFit = h2.Fit("gaus","S")
            chi2_nparams_gaus = (GausFit.Chi2(), GausFit.NFreeParameters())
            c1.SaveAs(outputLoc+"CH"+str(chan)+"_"+str(f)+".pdf")
            y.append((gaus.GetParameter(2))/1e-12)
            y_err.append((gaus.GetParError(2))/1e-12)
        c0 = TCanvas("c", "c", 800, 750)
        SetPadStyle(c0)
        c0.SetGridy()
        c0.SetGridx()
        gr = TGraphErrors(len(y),array('d',x),array('d',y),array('d',x_err),array('d',y_err))
        gr.SetMarkerColorAlpha(sensor[sen][1],0.8)
        gr.SetLineColor(sensor[sen][1])
        gr.SetMarkerStyle(sensor[sen][2])
        gr.SetMarkerSize(1.5)
        graphs.Add(gr)
        leg.AddEntry(gr,sensor[sen][0],"p")

    graphs.SetTitle(";CFD Fraction;Time Precision [ps]")
    c0.Update()
    graphs.Draw("AP same")
    leg.Draw("same")
    DrawCMSLabels(c0, '', 1)
    c0.SaveAs(outputLoc+"CH"+str(chan)+".pdf")
