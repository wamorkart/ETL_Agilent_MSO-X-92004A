from ROOT import *

inputLoc = '/afs/cern.ch/work/t/twamorka/ETL_FNAL/ETL_Agilent_MSO-X-92004A/Plotter/Sensor'
outputLoc = '/afs/cern.ch/user/t/twamorka/www/FNAL_ETL/'

doLanFit = True

Cut = 'amp[0]>150 && amp[3]>160 && amp[3]<210 && amp[0]<580'

Vars = []
Vars.append(['amp[0]','CH1_amp',';Channel 1 amplitude; Yields',100,-400,800])
Vars.append(['amp[1]','CH2_amp',';Channel 2 amplitude; Yields',100,-400,800])
Vars.append(['amp[2]','CH3_amp',';Channel 3 amplitude; Yields',100,-400,800])
Vars.append(['amp[3]','CH4_amp',';Channel 4 amplitude; Yields',100,-400,800])

cfdFrac = [5,10,15,20,25,30,35,40,45,50,55,60,65]

colors = [kRed,kBlue,kGreen]
markerStyle = [20,21,22]
senName = ['Pad 1','Pad 2','Pad 3']
