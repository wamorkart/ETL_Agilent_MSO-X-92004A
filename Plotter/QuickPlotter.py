from ROOT import *
 
from array import array

def SetAxisTextSizes(obj, extraoffy=0, extraoffx=0):
    obj.GetYaxis().SetTitleOffset(1.1+extraoffy)
    obj.GetYaxis().SetTitleSize(0.0425)
    obj.GetYaxis().SetLabelSize(0.04)
    obj.GetXaxis().SetTitleOffset(1.1+extraoffx)
    obj.GetXaxis().SetTitleSize(0.0425)
    obj.GetXaxis().SetLabelSize(0.04)
#try:
    #obj.GetZaxis().SetTitleOffset(1.1)
    #obj.GetZaxis().SetTitleSize(0.0425)
    #obj.GetZaxis().SetLabelSize(0.04)
#except AttributeError:
#a=1

def SetGeneralStyle():
    gStyle.SetFrameLineWidth(2)

def SetPadStyle(obj):
    obj.SetTicky()
    obj.SetTickx()

def DrawCMSLabels(obj, lumi, simul=0, left_border=0, size=0.045):
    #  obj.Print()
    pad = obj.cd()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    lat = TLatex()
    lat.SetTextSize(size)
    lat.SetTextAlign(11)
    lat.SetTextFont(42)
    cmsTag = "#bf{CMS} #it{Preliminary}"
    d1 = lat.DrawLatexNDC(l+0.01+left_border, 1-t+0.015, cmsTag)
    lat.SetTextAlign(31)
    Tag = 'FNAL TB'
    d2 = lat.DrawLatexNDC(1-r-0.001, 1-t+0.015, Tag)
    return [d1,d2]

graphs2  = TMultiGraph()
#leg2 = TLegend(0.6, 0.7, 0.89, 0.89)
leg2 = TLegend(0.156642, 0.693295, 0.447368, 0.883024)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.04)
leg2.SetFillColor(kWhite)
leg2.SetFillStyle(0)

## min time res values
array_res = [[39.237493023568724, 36.39048409549247, 33.21523335548811, 31.557967230465373, 29.778588245411846, 29.002657318238303],[63.73177987753874, 61.39381580954103, 57.007389129373166, 53.75726038322963, 51.567872952510236, 49.46039383898842],[ 65.51348877352999, 64.56393644056017, 64.36267971340018, 63.69119688210293],[37,39,39,36,39,39],[58,42,39,40,38]]
array_res_err = [[0.6174214102942219, 0.34816253596229413, 0.311471436773742, 0.35211025905455723, 0.2452456583166834, 0.19447829761169858],[1.3194336688032655, 0.5876334023265476, 0.5163287492373336, 0.5330258213555891, 0.39619005184244727, 0.2847851549254171],[2.388339468484104, 1.0337602624722417, 0.8541224663472495, 0.7590641830061642, 0.5698434424991936, 0.39074235705120597],[2,2,2,1,1,2],[4,2,1,2,1]]

##--mpv values
#array_res = [[56.8601157915048, 72.2077778214182, 85.88836961026001, 99.81787363407156, 125.07921748508402, 139.47685988128487],[12.297963388582918, 14.046547065305061, 15.746900057828212, 18.680710152844775, 20.16927402425084, 23.016116744729697],[3.009239104694401, 3.1122549871940657, 5.527979577754613, 5.153109875593491, 9.416216635840991, 12.412086967995375],[43.5,54.8,67.6,81.3,88.3,90.5],[24.2,30.3,40.7,61.2,73.6,83.9]]
#array_res_err = [[6.767247448121617, 8.123877056429295, 9.282428343956362, 4.571192775425379, 8.670164852682023, 8.764873456157058],[1.3890953706885345, 2.073259510849781, 2.5476311424649913, 2.716797914210329, 3.194726588687377, 3.3867730708732915],[0.42733734782192306, 0.45929730947311914, 0.6043586855355962, 0.5710247164349062, 1.9879064469157153, 1.636478476893002],[0.3,0.4,0.4,0.6,0.8,0.9],[0.3,0.4,0.6,0.8,0.8,0.7]]

##--noise values
array_res = [[1.4935166460701335, 1.5156781966332915, 1.4974437319626113, 1.5381241469319287, 1.6739299379962416, 1.965989730997486],[1.457658076486086, 1.4690223077927456, 1.4746038270125228, 1.5048354904148906, 1.502390817474152, 1.5133244508564088],[1.3880051054859697, 1.4149869018387387, 1.4109869764014547, 1.436851595389512, 1.4214960254316007, 1.4297197981177976],[1.6,1.9,2.4,2.6,2.8,3.4],[1.7,1.6,1.6,1.9,2.1,2.7]]
array_res_err = [[0.4094432874157068, 0.5384041151937187, 0.46083570701393817, 0.5524829138727316, 0.4664059047638065, 0.45360999736263524],[0.4020244998003423, 0.36560996056036976, 0.3759931945179505, 0.44682832927344107, 0.4108348563938528, 0.400177277808257],[0.40937191116516114, 0.46113460349070723, 0.40969252021492336, 0.5226473924800369, 0.4293513306735542, 0.43891204481470547],[0.5,0.6,0.7,0.7,0.8,0.9],[0.6,0.5,0.4,0.4,0.5,0.7]]

array_voltage = [[160,175,185,195,205,210],[500,550,575,600,615,630],[600,615,630,645],[450,475,500,525,535,545],[450,475,500,525,540]]
Bias_err = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0]]
colors = [kOrange+10,kMagenta,kBlack,kRed,kBlue,kGreen+4]
markerStyle = [33,34,29,20,21,22]
senName = ['HPK 4x4 Pre-rad','8e14','1.5e15','4E14','5E14']

for i in range(5):
    c2 = TCanvas("c", "c", 800, 750)
    SetPadStyle(c2)
    c2.SetGridy()
    c2.SetGridx()
    print array_res[i]
    print array_voltage[i]
    gr2 = TGraphErrors(len(array_voltage[i]),array('d',list(array_voltage[i])),array('d',list(array_res[i])),array('d',list(Bias_err[i])),array('d',list(array_res_err[i])))
    gr2.SetMarkerColorAlpha(colors[i],0.8)
    gr2.SetLineColor(colors[i])
    gr2.SetMarkerStyle(markerStyle[i])
    gr2.SetMarkerSize(1)
    graphs2.Add(gr2)
    leg2.AddEntry(gr2,senName[i],"lp")


#graphs2.SetTitle(";Bias Voltage [V];Time Resolution [ps]")
#graphs2.SetTitle(";Bias Voltage [V];MPV [mV]")
graphs2.SetTitle(";Bias Voltage [V];Noise [mV]")
graphs2.SetMinimum(0)
graphs2.SetMaximum(5)
#c2.Update()
graphs2.Draw("AP same")
#graphs2.GetYaxis().SetLimits(25,60)
#graphs2.GetXaxis().SetLimits(490,610)

leg2.Draw("same")
DrawCMSLabels(c2, '', 1)
c2.SaveAs("NoiseVsVoltage.pdf")
