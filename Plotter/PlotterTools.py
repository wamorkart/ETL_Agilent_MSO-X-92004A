from ROOT import *

inputLoc = '/home/daq/fnal_tb_18_11/LocalData/RECO'
outputLoc = '/home/daq/fnal_tb_18_11/LocalData/RECO/Plots/NewPlots/'

doLanFit = True

Cut = 'amp[0]>150 && amp[3]>160 && amp[3]<210 && amp[0]<580'
Cut1 = 'amp[0]>100 && amp[0]<260 && amp[1]>100 && amp[1]<260 && amp[2]>100 && amp[2]<260 && amp[3] > 100 && amp[3] < 400'
Cut2 = 'amp[0]>100 && amp[0]<350 && amp[1]>100 && amp[1]<350 && amp[2]>100 && amp[2]<350 && amp[3] > 100 && amp[3] < 400'
Cut3 = 'amp[0]>100 && amp[0]<400 && amp[1]>100 && amp[1]<400 && amp[2]>100 && amp[2]<400 && amp[3] > 100 && amp[3] < 400'
Cut4 = 'amp[0]>100 && amp[0]<600 && amp[1]>100 && amp[1]<600 && amp[2]>100 && amp[2]<600 && amp[3] > 100 && amp[3] < 400'
Cut5 = 'amp[0]>300 && amp[0]<850 && amp[1]>300 && amp[1]<850 && amp[2]>300 && amp[2]<850 && amp[3] > 100 && amp[3] < 360'

Vars = []
Vars.append(['amp[0]','CH1_amp',';Channel 1 amplitude; Yields',100,0,1000])
Vars.append(['amp[1]','CH2_amp',';Channel 2 amplitude; Yields',100,0,1000])
Vars.append(['amp[2]','CH3_amp',';Channel 3 amplitude; Yields',100,0,1000])
Vars.append(['amp[3]','CH4_amp',';Channel 4 amplitude; Yields',100,0,1000])

cfdFrac = [5,10,15,20,25,30,35,40,45,50,55,60,65]

colors = [kRed,kBlue,kGreen+4]
markerStyle = [20,21,22]
senName = ['Pad 1','Pad 2','Pad 3']
