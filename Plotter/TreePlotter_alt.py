from PlotterTools import *
from ROOT import *
import math
import optparse
import argparse
from array import array
#import numpy as np
from MyCMSStyle import *
gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetOptFit()

parser = argparse.ArgumentParser(description='Plotter')

parser.add_argument('--Range1', metavar='Range1', type=str, nargs = '+', help='Run Number for bias range 1',required=False)
parser.add_argument('--Range2', metavar='Range2', type=str, nargs = '+', help='Run Number for bias range 2',required=False)
parser.add_argument('--Range3', metavar='Range3', type=str, nargs = '+', help='Run Number for bias range 3',required=False)
parser.add_argument('--Range4', metavar='Range4', type=str, nargs = '+', help='Run Number for bias range 4',required=False)
parser.add_argument('--Range5', metavar='Range5', type=str, nargs = '+', help='Run Number for bias range 5',required=False)

parser.add_argument('--Channel', metavar='Channel', type=str, nargs = '+', help='Channel Number',required=False)
# parser.add_argument('--Bias', metavar='Bias', type=str, nargs = '+', help='Bias voltage',required=False)
args = parser.parse_args()

Runlist = []
Runlist.append([int(args.Range1[0]),int(args.Range1[1])])
Runlist.append([int(args.Range2[0]),int(args.Range2[1])])
Runlist.append([int(args.Range3[0]),int(args.Range3[1])])
Runlist.append([int(args.Range4[0]),int(args.Range4[1])])
Runlist.append([int(args.Range5[0]),int(args.Range5[1])])

res_2d = []
res_2d_err = []
Voltage = []
Voltage_err = []
Bias_values = []
Bias_err = []
Signal_2d = []
Signal_2d_err = []
Noise_2d = []
Noise_2d_err = []
SignaloverNoise_2d = []

trees = []
for run in Runlist:
    tempChain = TChain('pulse')
    minrun = run[0]
    maxrun = run[1]
    while minrun < maxrun + 1:
        tempChain.Add(str('NetScopeStandalone/v3/run_scope'+str(minrun)+'_converted.root'))
        minrun += 1
    trees.append(tempChain)

Voltage.append([60,500,650,3800]) #Range 1
Voltage.append([60,550,675,3800]) #Range 2
Voltage.append([65,575,0,3800]) #Range 3
Voltage.append([55,590,0,3800]) #Range 4
Voltage.append([67,600,0,3800]) #Range 5

# print len(Voltage)
# print len(run)

for t, tree in enumerate(trees):
    print tree.GetEntries()
    MPV_Values = []
    MPV_Values_err = []
    BaselineRMS_Mean = []
    BaselineRMS_StdDev = []
    # for chan in range(len(args.Channel)):
    for v, var in enumerate(Vars):
        hist = "chan_"+str(var[1])
        Cut = ""
        if "amp" in var[0]:
            Cut = (Cut_forAmp2[v][t])

        h = TH1F(hist, "Amplitude; "+var[1]+";Yields",var[3], var[4], var[5])
        tree.Draw(var[0]+'>>'+hist,TCut(Cut))
        h.SetLineColor(kBlack)
        h.SetLineWidth(2)
        h.GetYaxis().SetTitleOffset(1.5)
        c = TCanvas('c', 'c', 800, 600)
        h.Draw()
        lat = TLatex()
        lat.SetNDC()
        lat.SetTextColor(kBlack)
        lat.SetTextAlign(11)
        lat.SetTextFont(63)
        lat.SetTextSize(25)
        Tag = "Bias = " + str(Voltage[t]) +"V" + "  " + str(Cut)
        lat.DrawLatex(0.11,0.91,Tag)
        c.Update()
        # c.SaveAs(outputLoc+"Range_"+str(t)+"_"+str(var[1])+"_WithCuts.pdf")
        # c.SetLogy()
        # c.SaveAs(outputLoc+"Range_"+str(t)+"_"+str(var[1])+"_WithCuts_Log.pdf")
        if doLanFit and "amp" in var[0]: ##--Landau fit of amplitude distribution
           lanfit = TF1(var[1]+hist,"landau",0, 900)
           h.Fit(var[1]+hist,"R")
           MPV_Values.append(lanfit.GetParameter(1))
           MPV_Values_err.append(lanfit.GetParameter(2))
           c.Draw()
           c.SaveAs(outputLoc+"Range_"+str(t)+"_fitLan_"+str(var[1])+".pdf")

        if "baseline" in var[0]:
            BaselineRMS_Mean.append(h.GetMean())
            BaselineRMS_StdDev.append(math.sqrt(h.GetMean()))
            # c.SaveAs(outputLoc+"Range_"+str(t)+"_"+str(var[1])+".pdf")
    Signal_2d.append(MPV_Values)
    Signal_2d_err.append(MPV_Values_err)
    Noise_2d.append(BaselineRMS_Mean)
    Noise_2d_err.append(BaselineRMS_StdDev)
    SignaloverNoise_2d.append([float(ai/bi) for ai, bi in zip(MPV_Values, BaselineRMS_Mean)])

    graphs = TMultiGraph()
    leg = TLegend(0.6, 0.7, 0.89, 0.89)
    # leg  = TLegend(0.1,0.7,0.48,0.9)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.02)
    leg.SetFillColor(kWhite)
    leg.SetFillStyle(0)

    res_min = []
    res_min_err = []

    bias = []
    bias_err = []
#
#     # print "VOLTAGE IS ", Voltage[t]
#
    for chan in range(len(args.Channel)):
        y =[]
        y_err = []
        x = cfdFrac
        x_err = []
        Cut_res = Cut_forAmp2[chan][t]+"&& amp[3] > 165 && amp[3] < 230"
        for f in cfdFrac:
            hist2 = "Range_"+str(t)+"Ch"+str(args.Channel[chan])+"_"+str(f)
            Tag = str(Cut_res)
            h2 = TH1F(hist2,"Time Resolution  "+Tag+"; #Delta T CH"+str(args.Channel[chan])+"_"+str(f)+";Yields" , 150, 7.6e-09, 8.6e-09)
            tree.Draw("LP2_"+str(f)+"["+str(args.Channel[chan])+"]"+"-LP2_30[3]>>"+hist2, TCut(Cut_res))
            c1 = TCanvas('c1', 'c1', 800, 600)
            h2.Draw()
            # lat = TLatex()
            # lat.SetNDC()
            # lat.SetTextColor(kBlack)
            # lat.SetTextAlign(11)
            # lat.SetTextFont(63)
            # lat.SetTextSize(25)
            # Tag = str(Cut_res)
            # lat.DrawLatex(0.11,0.91,Tag)
            gausfit = TF1("f"+hist2,"gaus",7e-09, 11e-09)
            h2.Fit("f"+hist2,"R")
            c1.SaveAs(outputLoc+"Range_"+str(t)+"_CH"+str(args.Channel[chan])+"_CFD_"+str(f)+".pdf")
            y.append((gausfit.GetParameter(2))/1e-12)
            y_err.append((gausfit.GetParError(2))/1e-12)
            x_err.append(0)
        bias.append(Voltage[t][chan])
        # bias_err.append(0)
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
    Bias_values.append(bias)
    Bias_err.append(0)
    graphs.SetTitle(";CFD Fraction;Time Resolution [ps]")
    graphs.SetMinimum(30)
    graphs.SetMaximum(150)
    c0.Update()
    graphs.Draw("AP same")
    leg.Draw("same")
    DrawCMSLabels(c0, '', 1)
    c0.SaveAs(outputLoc+"Range_"+str(t)+"_ResVSCFD.pdf")

res_2d_transposed = zip(*res_2d)
res_2d_err_transposed = zip(*res_2d_err)

bias_transposed = zip(*Bias_values)

graphs2  = TMultiGraph()
leg2 = TLegend(0.6, 0.7, 0.89, 0.89)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.04)
leg2.SetFillColor(kWhite)
leg2.SetFillStyle(0)

Signal_2d_transposed = zip(*Signal_2d)
Signal_2d_err_transposed = zip(*Signal_2d_err)
Noise_2d_transposed = zip(*Noise_2d)
Noise_2d_err_transposed = zip(*Noise_2d_err)
SignaloverNoise_2d_transposed = zip(*SignaloverNoise_2d)

graphs3  = TMultiGraph()
leg3 = TLegend(0.6, 0.7, 0.89, 0.89)
leg3.SetBorderSize(0)
leg3.SetTextSize(0.02)
leg3.SetFillColor(kWhite)
leg3.SetFillStyle(0)

graphs4  = TMultiGraph()
leg4 = TLegend(0.6, 0.7, 0.89, 0.89)
leg4.SetBorderSize(0)
leg4.SetTextSize(0.02)
leg4.SetFillColor(kWhite)
leg4.SetFillStyle(0)

graphs5  = TMultiGraph()
leg5 = TLegend(0.6, 0.7, 0.89, 0.89)
leg5.SetBorderSize(0)
leg5.SetTextSize(0.02)
leg5.SetFillColor(kWhite)
leg5.SetFillStyle(0)




for i in range(len(args.Channel)):
    c2 = TCanvas("c", "c", 800, 750)
    SetPadStyle(c2)
    c2.SetGridy()
    c2.SetGridx()
    gr2 = TGraphErrors(len(Runlist),array('d',list(bias_transposed[i])),array('d',list(res_2d_transposed[i])),array('d',list(Bias_err)),array('d',list(res_2d_err_transposed[i])))
    gr2.SetMarkerColorAlpha(colors[i],0.8)
    gr2.SetLineColor(colors[i])
    gr2.SetMarkerStyle(markerStyle[i])
    gr2.SetMarkerSize(1.5)
    graphs2.Add(gr2)
    if i == 0 or i == 2:
        continue
    elif i == 1:
         leg2.AddEntry(gr2,senName[i],"lp")

    # gr3 = TGraphErrors(len(Runlist),array('d',list(bias_transposed[i])),array('d',list(Signal_2d_transposed[i])),array('d',list(Bias_err)),array('d',list(Signal_2d_err_transposed[i])))
    # gr3.SetMarkerColorAlpha(colors[i],0.8)
    # gr3.SetMarkerStyle(markerStyle[i])
    # graphs3.Add(gr3)
    # leg3.AddEntry(gr3,senName[i],"lp")
    #
    # gr4 = TGraphErrors(len(Runlist),array('d',list(bias_transposed[i])),array('d',list(Noise_2d_transposed[i])),array('d',list(Bias_err)),array('d',list(Noise_2d_err_transposed[i])))
    # gr4.SetMarkerColorAlpha(colors[i],0.8)
    # gr4.SetLineColor(colors[i])
    # gr4.SetMarkerStyle(markerStyle[i])
    # gr4.SetMarkerSize(1.5)
    # graphs4.Add(gr4)
    # leg4.AddEntry(gr4,senName[i],"lp")
    #
    # gr5 = TGraph(len(Runlist),array('d',list(bias_transposed[i])),array('d',list(SignaloverNoise_2d_transposed[i])))
    # gr5.SetMarkerColorAlpha(colors[i],0.8)
    # gr5.SetLineColor(colors[i])
    # gr5.SetMarkerStyle(markerStyle[i])
    # gr5.SetMarkerSize(1.5)
    # graphs5.Add(gr5)
    # leg5.AddEntry(gr5,senName[i],"lp")

graphs2.SetTitle(";Bias Voltage [V];Time Resolution [ps]")
graphs2.SetMinimum(25)
graphs2.SetMaximum(60)
c2.Update()
graphs2.Draw("AP same")
# graphs2.GetYaxis().SetLimits(25,60)
graphs2.GetXaxis().SetLimits(490,610)

leg2.Draw("same")
DrawCMSLabels(c2, '', 1)
c2.SaveAs(outputLoc+"MinResVsVoltage.pdf")

# graphs3.SetTitle(";Bias Voltage [V]; Signal")
# c2.Update()
# graphs3.Draw("AP same")
# graphs3.GetXaxis().SetLimits(50,70)
# leg3.Draw("same")
# DrawCMSLabels(c2, '', 1)
# c2.SaveAs(outputLoc+"SignalVsVoltage.pdf")
#
# graphs4.SetTitle(";Bias Voltage [V]; Noise")
# c2.Update()
# graphs4.Draw("AP same")
# # graphs4.GetXaxis().SetLimits(50,70)
# graphs4.GetXaxis().SetLimits(480,620)
# leg4.Draw("same")
# DrawCMSLabels(c2, '', 1)
# c2.SaveAs(outputLoc+"NoiseVsVoltage.pdf")
#
# graphs5.SetTitle(";Bias Voltage [V]; Signal/Noise")
# c2.Update()
# graphs5.Draw("AP same")
# graphs5.GetXaxis().SetLimits(480,620)
# leg5.Draw("same")
# DrawCMSLabels(c2, '', 1)
# c2.SaveAs(outputLoc+"SignaloverNoiseVsVoltage.pdf")
