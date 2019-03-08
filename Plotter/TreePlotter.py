from PlotterTools import *
from ROOT import *
import optparse
import argparse
from array import array
import numpy as np
from MyCMSStyle import *
gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetOptFit()

parser = argparse.ArgumentParser(description='Plotter')

parser.add_argument('--Run', metavar='Run', type=str, nargs = '+', help='Run Number',required=False)
parser.add_argument('--Channel', metavar='Channel', type=str, nargs = '+', help='Channel Number',required=True)
parser.add_argument('--Bias', metavar='Bias', type=str, nargs = '+', help='Bias voltage',required=True)
args = parser.parse_args()

res_2d = []
res_2d_err = []
Voltage = []
Voltage_err = []

for bias in range(len(args.Bias)):
    ch = TChain('pulse')
    ch.Add(str('Bias_'+str(args.Bias[bias])+'/run_scope*_converted.root'))
    Voltage.append(float(args.Bias[bias]))
    Voltage_err.append(float(0))
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
        c.SaveAs("Bias"+str(args.Bias[bias])+"_"+str(var[1])+".pdf")

        if doLanFit and "amp" in var[0]: ##--Landau fit of amplitude distribution
           fitResultPtr_lan = h.Fit("landau","S")
           chi2_nparams_lan = (fitResultPtr_lan.Chi2(), fitResultPtr_lan.NFreeParameters())
           c.Draw()
           c.SaveAs("Bias"+str(args.Bias[bias])+"_fitLan_"+str(var[1])+".pdf")

    graphs = TMultiGraph()
    leg = TLegend(0.6, 0.7, 0.89, 0.89)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.02)
    leg.SetFillColor(kWhite)

    res_min = []
    res_min_err = []
    for chan in range(len(args.Channel)):
        y =[]
        y_err = []
        x = cfdFrac
        x_err = []
        for f in cfdFrac:
            hist2 = "Ch"+str(chan)+"_"+str(f)
            h2 = TH1F(hist2,"Time Resolution; #Delta T CH"+str(args.Channel[chan])+"_"+str(f)+";Yields" , 100, 5e-09, 6e-09)
            ch.Draw("LP2_"+str(f)+"["+str(args.Channel[chan])+"]"+"-LP2_50[3]"+'>>'+hist2)
            c1 = TCanvas('c1', 'c1', 800, 600)
            GausFit = h2.Fit("gaus","S")
            chi2_nparams_gaus = (GausFit.Chi2(), GausFit.NFreeParameters())
            c1.SaveAs("Bias"+str(args.Bias[bias])+"CH"+str(args.Channel[chan])+"_CFD_"+str(f)+".pdf")
            y.append((gaus.GetParameter(2))/1e-12)
            y_err.append((gaus.GetParError(2))/1e-12)
            x_err.append(0)

        res_min.append(min(y))
        res_min_err.append(y_err[min(xrange(len(y)), key=y.__getitem__)])
        c0 = TCanvas("c", "c", 800, 750)
        SetPadStyle(c0)
        c0.SetGridy()
        c0.SetGridx()
        gr = TGraphErrors(len(y),array('d',x),array('d',y),array('d',x_err),array('d',y_err))
        gr.SetMarkerColorAlpha(colors[chan],0.8)
        gr.SetLineColor(colors[chan])
        gr.SetMarkerStyle(markerStyle[chan])
        gr.SetMarkerSize(1.5)
        graphs.Add(gr)
        leg.AddEntry(gr,senName[chan],"lp")

    res_2d.append(res_min)
    res_2d_err.append(res_min_err)

    graphs.SetTitle(";CFD Fraction;Time Resolution [ps]")
    c0.Update()
    graphs.Draw("AP same")
    leg.Draw("same")
    DrawCMSLabels(c0, '', 1)
    c0.SaveAs("Bias"+str(args.Bias[bias])+"_ResVSCFD.pdf")

res_2d_transposed = zip(*res_2d)
res_2d_err_transposed = zip(*res_2d_err)
graphs2  = TMultiGraph()
leg2 = TLegend(0.6, 0.7, 0.89, 0.89)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.02)
leg2.SetFillColor(kWhite)

for i in range(len(res_2d_transposed[0])):
    c2 = TCanvas("c", "c", 800, 750)
    SetPadStyle(c2)
    c2.SetGridy()
    c2.SetGridx()
    gr2 = TGraphErrors(len(Voltage),array('d',Voltage),array('d',list(res_2d_transposed[i])),array('d',Voltage_err),array('d',list(res_2d_err_transposed[i])))
    gr2.SetMarkerColorAlpha(colors[i],0.8)
    gr2.SetLineColor(colors[i])
    gr2.SetMarkerStyle(markerStyle[i])
    gr2.SetMarkerSize(1.5)
    graphs2.Add(gr2)
    leg2.AddEntry(gr2,senName[i],"lp")

graphs2.SetTitle(";Bias Voltage [V];Time Resolution [ps]")
c2.Update()
graphs2.Draw("AP same")
leg2.Draw("same")
DrawCMSLabels(c2, '', 1)
c2.SaveAs("MinResVsVoltage.pdf")
