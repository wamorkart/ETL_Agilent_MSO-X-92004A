from ROOT import *

inputLoc = '/home/daq/fnal_tb_18_11/LocalData/RECO'
#outputLoc = '/home/daq/fnal_tb_18_11/LocalData/RECO/Plots/NewPlots/'
#outputLoc = '/home/daq/fnal_tb_18_11/LocalData/RECO/Plots/NewPlots_14March/'
outputLoc = '/home/daq/fnal_tb_18_11/LocalData/RECO/Plots/'
doLanFit = True
doLanGausFit = False

Cut_forAmp = [] ## For parasitic TB (March 2019): Data1
# per channel [for bias = 100V, 125 V, 150V, 175V, 200V]
Cut_forAmp.append(["amp[0] > 50 && amp[0] < 260 ","amp[0] > 80 && amp[0] < 340 ","amp[0] > 100 && amp[0] < 440 ","amp[0] > 150 && amp[0] < 600 ","amp[0] > 300 && amp[0] < 780 "])
Cut_forAmp.append(["amp[1] > 50 && amp[1] < 260 ","amp[1] > 80 && amp[1] < 340 ","amp[1] > 100 && amp[1] < 440 ","amp[1] > 150 && amp[1] < 600 ","amp[1] > 300 && amp[1] < 780 "])
Cut_forAmp.append(["amp[2] > 50 && amp[2] < 260 ","amp[2] > 80 && amp[2] < 340 ","amp[2] > 100 && amp[2] < 440 ","amp[2] > 150 && amp[2] < 600 ","amp[2] > 300 && amp[2] < 780 "])
Cut_forAmp.append(["amp[3] > 125 && amp[3] < 200 ","amp[3] > 125 && amp[3] < 200 ","amp[3] > 125 && amp[3] < 200 ","amp[3] > 125 && amp[3] < 200 ","amp[3] > 125 && amp[3] < 200 "])

Cut_forAmp2 = [] ## For parasitic TB (March 2019): Data2
Cut_forAmp2.append(["amp[0] > 20 && amp[0] < 80 ","amp[0] > 20 && amp[0] < 80 ","amp[0] > 30 && amp[0] < 85 ","amp[0] > 200 ","amp[0] > 40 && amp[0] < 100 "])
Cut_forAmp2.append(["amp[1] > 12 && amp[1] < 50 ","amp[1] > 15 && amp[1] < 60 ","amp[1] > 18 && amp[1] < 90 ","amp[1] > 18 && amp[1] < 90 ","amp[1] > 18 && amp[1] < 90 "])
Cut_forAmp2.append(["amp[2] > 48 && amp[2] < 85 ","amp[2] > 58 && amp[2] < 88 ","amp[2] > 200 ","amp[2] > 200 ","amp[2] > 200"])
Cut_forAmp2.append(["amp[3] > 165 && amp[3] < 230 ","amp[3] > 165 && amp[3] < 230 ","amp[3] > 165 && amp[3] < 230 ","amp[3] > 165 && amp[3] < 230 ","amp[3] > 165 && amp[3] < 230 "])


#Cut = 'amp[0]>150 && amp[3]>160 && amp[3]<210 && amp[0]<580'_Mar28
Cut1 = 'amp[0]>100 && amp[0]<260 && amp[1]>100 && amp[1]<260 && amp[2]>100 && amp[2]<260 && amp[3] > 100 && amp[3] < 400'
Cut2 = 'amp[0]>100 && amp[0]<350 && amp[1]>100 && amp[1]<350 && amp[2]>100 && amp[2]<350 && amp[3] > 100 && amp[3] < 400'
Cut3 = 'amp[0]>100 && amp[0]<400 && amp[1]>100 && amp[1]<400 && amp[2]>100 && amp[2]<400 && amp[3] > 100 && amp[3] < 400'
Cut4 = 'amp[0]>100 && amp[0]<600 && amp[1]>100 && amp[1]<600 && amp[2]>100 && amp[2]<600 && amp[3] > 100 && amp[3] < 400'
Cut5 = 'amp[0]>300 && amp[0]<850 && amp[1]>300 && amp[1]<850 && amp[2]>300 && amp[2]<850 && amp[3] > 100 && amp[3] < 360'

Vars = []
Vars.append(['amp[0]','CH0_amp',';Channel 0 amplitude; Yields',100,0,200])
Vars.append(['amp[1]','CH1_amp',';Channel 1 amplitude; Yields',100,0,200])
Vars.append(['amp[2]','CH2_amp',';Channel 2 amplitude; Yields',100,0,200])
Vars.append(['amp[3]','CH3_amp',';Channel 3 amplitude; Yields',100,-10,500])

Vars.append(['baseline_RMS[0]','CH0_baselineRMS',';Channel 0 Baseline RMS; Yields',100,0,10])
Vars.append(['baseline_RMS[1]','CH1_baselineRMS',';Channel 1 Baseline RMS; Yields',100,0,10])
Vars.append(['baseline_RMS[2]','CH2_baselineRMS',';Channel 2 Baseline RMS; Yields',100,0,10])
Vars.append(['baseline_RMS[3]','CH3_baselineRMS',';Channel 3 Baseline RMS; Yields',100,0,10])


cfdFrac = [5,10,15,20,25,30,35,40,45,50,55,60,65]

# cfdFrac = [50,55,60,65]
colors = [kRed,kBlue,kGreen+4]
markerStyle = [20,21,22]
# senName = ['Pad 1','Pad 2','Pad 3']
# senName = ['1.5E15']
senName = ['Pre-rad sensor','1.5e15','3e15']


f_conv = TF1Convolution("landau", "gaus", -10, 10, kTRUE)
f_conv.SetRange(-2, 2)
f_conv.SetNofPointsFFT(1000)
        # print(f_conv.GetNpar())
fitfunction_conv = TF1("fitfunction_conv", f_conv, -2, 2, f_conv.GetNpar())
