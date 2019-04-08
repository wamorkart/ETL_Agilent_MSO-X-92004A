from PlotterTools import *
from ROOT import *
import optparse
import argparse
from array import array
#import numpy as np
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
    #ch.Add(str('/home/daq/fnal_tb_18_11/LocalData/RECO/NetScopeStandalone/v3/run_scope*_converted.root'))
    ch.Add(str('Bias_'+str(args.Bias[bias])+'/run_scope*_converted.root'))
    Voltage.append(float(args.Bias[bias]))
    Voltage_err.append(float(0))
    for var in Vars:
        hist = var[1]
        h = TH1F(hist, var[2], var[3], var[4], var[5])
        #tempCut = TCut(Cut)
        #if "amp" in var[0] and bias == '100':
            #Cut = "amp[0]>50 && amp[0] < 250"
        # Cut = var[0] + "> 50 &&" + var[0] + "< 250 && amp[3] > 100 && amp[3] < 300"
        if args.Bias[bias] == '100':
            Cut = var[0] + "> 50 && " + var[0] + "< 250"
            if "CH3" in var[1]:
                Cut = "amp[3]> 50 && amp[3]< 350"
        elif args.Bias[bias] == '125':
            Cut = var[0] + "> 70 && " + var[0] + "< 350"
        elif args.Bias[bias] == '150':
            Cut = var[0] + "> 80 && " + var[0] + "< 350"
        else: Cut = "1>0"
        print "Cut is ", Cut
        ch.Draw(var[0]+'>>'+hist, TCut(Cut))
        h.SetLineColor(kBlack)
        h.SetLineWidth(2)
        h.GetYaxis().SetTitleOffset(1.5)
        c = TCanvas('c', 'c', 800, 600)
        h.Draw()
        c.SaveAs(outputLoc+"Bias"+str(args.Bias[bias])+"_"+str(var[1])+".pdf")

        if doLanFit and "amp" in var[0]: ##--Landau fit of amplitude distribution
           fitResultPtr_lan = h.Fit("landau","S")
           chi2_nparams_lan = (fitResultPtr_lan.Chi2(), fitResultPtr_lan.NFreeParameters())
           c.Draw()
           c.SaveAs(outputLoc+"Bias"+str(args.Bias[bias])+"_fitLan_"+str(var[1])+".pdf")
#
#     graphs = TMultiGraph()
#     leg = TLegend(0.6, 0.7, 0.89, 0.89)
#     leg.SetBorderSize(0)
#     leg.SetTextSize(0.02)
#     leg.SetFillColor(kWhite)
#     leg.SetFillStyle(0)
#
#     res_min = []
#     res_min_err = []
#     #print range(len(args.Channel))
#     for chan in range(len(args.Channel)):
#         y =[]
#         y_err = []
#         x = cfdFrac
#         x_err = []
#         #print "channel ", str(args.Channel[chan])
#         for f in cfdFrac:
#             hist2 = "Ch"+str(args.Channel[chan])+"_"+str(f)
#             print "hist2 ", hist2
#             h2 = TH1F(hist2,"Time Resolution; #Delta T CH"+str(args.Channel[chan])+"_"+str(f)+";Yields" , 100, 5.0e-09, 5.9e-09)
#             if (args.Bias[bias] == '100'):
#                tempCut = 'amp['+str(args.Channel[chan])+']>50 && amp['+str(args.Channel[chan])+']<260 && amp[3] > 100 && amp[3] < 400'
#             elif (args.Bias[bias] == '125'):
#                tempCut = 'amp['+str(args.Channel[chan])+']>50 && amp['+str(args.Channel[chan])+']<350 && amp[3] > 100 && amp[3] < 170'
#             elif (args.Bias[bias] == '150'):
#                tempCut = 'amp['+str(args.Channel[chan])+']>50 && amp['+str(args.Channel[chan])+']<400 && amp[3] > 100 && amp[3] < 170'
#             elif (args.Bias[bias] == '175'):
#                tempCut = 'amp['+str(args.Channel[chan])+']>100 && amp['+str(args.Channel[chan])+']<600 && amp[3] > 100 && amp[3] < 170'
#             #else: tempCut = 'amp['+str(chan)+']>300 && amp['+str(chan)+']<850 && amp[3] > 100 && amp[3] < 360'
#             else: tempCut = 'amp['+str(args.Channel[chan])+']>320 && amp['+str(args.Channel[chan])+']<880 && amp[3] > 130 && amp[3] < 170'
#             TempCut = TCut(tempCut)
#             print "Cut ", tempCut
#             print "LP2_"+str(f)+"["+str(args.Channel[chan])+"]"+"-LP2_50[3]"
#             ch.Draw("LP2_"+str(f)+"["+str(args.Channel[chan])+"]"+"-LP2_50[3]>>"+hist2, TempCut)
#             #print ch.GetEntries()
#             c1 = TCanvas('c1', 'c1', 800, 600)
#             h2.Draw()
#             GausFit = h2.Fit("gaus","S")
#             chi2_nparams_gaus = (GausFit.Chi2(), GausFit.NFreeParameters())
#             c1.SaveAs(outputLoc+"Bias"+str(args.Bias[bias])+"_CH"+str(args.Channel[chan])+"_CFD_"+str(f)+".pdf")
#             y.append((gaus.GetParameter(2))/1e-12)
#             y_err.append((gaus.GetParError(2))/1e-12)
#             x_err.append(0)
#
#         res_min.append(min(y))
#         res_min_err.append(y_err[min(xrange(len(y)), key=y.__getitem__)])
#         c0 = TCanvas("c", "c", 800, 750)
#         SetPadStyle(c0)
#         c0.SetGridy()
#         c0.SetGridx()
#         gr = TGraphErrors(len(y),array('d',x),array('d',y),array('d',x_err),array('d',y_err))
#         gr.SetMarkerColorAlpha(colors[chan],0.8)
#         gr.SetLineColor(colors[chan])
#         gr.SetMarkerStyle(markerStyle[chan])
#         gr.SetMarkerSize(1.5)
#         graphs.Add(gr)
#         leg.AddEntry(gr,senName[chan],"lp")
#
#     res_2d.append(res_min)
#     res_2d_err.append(res_min_err)
#
#     graphs.SetTitle(";CFD Fraction;Time Resolution [ps]")
#     c0.Update()
#     graphs.Draw("AP same")
#     leg.Draw("same")
#     DrawCMSLabels(c0, '', 1)
#     c0.SaveAs(outputLoc+"Bias"+str(args.Bias[bias])+"_ResVSCFD.pdf")
#
# res_2d_transposed = zip(*res_2d)
# res_2d_err_transposed = zip(*res_2d_err)
#
# graphs2  = TMultiGraph()
# leg2 = TLegend(0.6, 0.7, 0.89, 0.89)
# leg2.SetBorderSize(0)
# leg2.SetTextSize(0.02)
# leg2.SetFillColor(kWhite)
# leg2.SetFillStyle(0)
#
# for i in range(len(args.Channel)):
#     c2 = TCanvas("c", "c", 800, 750)
#     SetPadStyle(c2)
#     c2.SetGridy()
#     c2.SetGridx()
#     gr2 = TGraphErrors(len(Voltage),array('d',Voltage),array('d',list(res_2d_transposed[i])),array('d',Voltage_err),array('d',list(res_2d_err_transposed[i])))
#     gr2.SetMarkerColorAlpha(colors[i],0.8)
#     gr2.SetLineColor(colors[i])
#     gr2.SetMarkerStyle(markerStyle[i])
#     gr2.SetMarkerSize(1.5)
#     graphs2.Add(gr2)
#     leg2.AddEntry(gr2,senName[i],"lp")
#
# graphs2.SetTitle(";Bias Voltage [V];Time Resolution [ps]")
# c2.Update()
# graphs2.Draw("AP same")
# leg2.Draw("same")
# DrawCMSLabels(c2, '', 1)
# c2.SaveAs(outputLoc+"MinResVsVoltage.pdf")
