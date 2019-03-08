from ROOT import *

inputLoc = '/afs/cern.ch/work/t/twamorka/ETL_FNAL/ETL_Agilent_MSO-X-92004A/Plotter/Sensor'
# sensor1Loc = '/afs/cern.ch/work/t/twamorka/ETL_FNAL/ETL_Agilent_MSO-X-92004A/Plotter/Sensor1/'
# sensor2Loc = '/afs/cern.ch/work/t/twamorka/ETL_FNAL/ETL_Agilent_MSO-X-92004A/Plotter/Sensor2/'
#
# bias1 = sensor1Loc+'Bias_'+
# Sensor = []
# Sensor.append([sensor1Loc,'Sensor 1',kRed,20])
# Sensor.append([sensor2Loc,'Sensor 2',kBlue,21])

##--Begin
# outputLoc = '/afs/cern.ch/user/t/twamorka/www/FNAL_ETL/'
doLanFit = True
#
Cut = 'amp[0]>150 && amp[3]>160 && amp[3]<210 && amp[0]<580'
#
Vars = []
Vars.append(['amp[0]','CH1_amp',';Channel 1 amplitude; Yields',100,-400,800])
Vars.append(['amp[1]','CH2_amp',';Channel 2 amplitude; Yields',100,-400,800])
Vars.append(['amp[2]','CH3_amp',';Channel 3 amplitude; Yields',100,-400,800])
Vars.append(['amp[3]','CH4_amp',';Channel 4 amplitude; Yields',100,-400,800])

cfdFrac = [5,10,15,20,25,30,35,40,45,50,55,60,65]

colors = [kRed,kBlue,kGreen]
markerStyle = [20,21,22]
senName = ['Pad 1','Pad 2','Pad 3']
#
# sensor1Loc = '/afs/cern.ch/work/t/twamorka/ETL_FNAL/ETL_Agilent_MSO-X-92004A/Plotter/'
# sensor2Loc = '/afs/cern.ch/work/t/twamorka/ETL_FNAL/ETL_Agilent_MSO-X-92004A/Plotter/'
#
# sensor = []
# sensor.append([sensor1Loc,'Sensor1',kRed,20])
# sensor.append([sensor2Loc,'Sensor2',kBlue,21])

##--End
