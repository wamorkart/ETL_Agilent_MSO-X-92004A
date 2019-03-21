# adapted for MSO-X 92004A

"""
VISA Control: FastFrame Acquisition
Tektronix DPO7254 Control
FNAL November 2018
CMS MTD ETL Test beam
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import optparse
import argparse
import signal
import os
import shutil
import datetime
from shutil import copy

stop_asap = False

import visa

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        shutil.copytree(item, d, symlinks, ignore)
def copynew(source,destination):
    for files in source:
        shutil.copy(files,destination)

"""#################SEARCH/CONNECT#################"""
# establish communication with dpo
rm = visa.ResourceManager()
dpo = rm.open_resource('TCPIP::192.168.133.161::INSTR')
dpo.timeout = 3000000
dpo.encoding = 'latin_1'
print(dpo.query('*idn?'))

parser = argparse.ArgumentParser(description='Run info.')

parser.add_argument('--numEvents',metavar='Events', type=str,default = 500, help='numEvents (default 500)',required=False)
parser.add_argument('--trigCh',metavar='trigCh', type=str, default='AUX',help='trigger Channel (default Aux (-0.1V))',required=False)
parser.add_argument('--trig',metavar='trig', type=float, default= -0.05, help='trigger value in V (default Aux (-0.05V))',required=False)
parser.add_argument('--trigSlope',metavar='trigSlope', type=str, default= 'NEGative', help='trigger slope; positive(rise) or negative(fall)',required=False)

args = parser.parse_args()
trigCh = 'CHANnel'+str(args.trigCh)
trigLevel = float(args.trig)
triggerSlope = args.trigSlope

date = datetime.datetime.now()

"""#################CONFIGURE INSTRUMENT#################"""
# variables for individual settings
hScale = 100e-9 # horizontal scale in seconds
numEvents = int(args.numEvents) # number of events for each file

#vertical scale
vScale_ch1 = 0.05 # in Volts for division
vScale_ch2 = 0.1 # in Volts for division
vScale_ch3 = 0.01 # in Volts for division
vScale_ch4 = 1 # in Volts for division

#vertical position
vPos_ch1 = 4  # in Divisions
vPos_ch2 = 4  # in Divisions
vPos_ch3 = 4  # in Divisions
vPos_ch4 = 4  # in Divisions

date = datetime.datetime.now()

"""#################CONFIGURE RUN NUMBER#################"""
# increment the last runNumber by 1
with open('runNumber.txt') as file:
    runNumber = int(file.read())
print('######## Starting RUN {} ########\n'.format(runNumber))
print('---------------------\n')
print(date)
print('---------------------\n')

with open('runNumber.txt','w') as file:
    file.write(str(runNumber+1))

"""#################SET THE OUTPUT FOLDER#################"""
# The scope save runs localy on a shared folder with
# path = r"C:\Users\Public\Documents\Infiniium\Test_Feb18"
path = r"C:\Users\Public\Documents\Infiniium\Test_March21"
dpo.write(':DISK:MDIRectory "{}"'.format(path))
log_path = "Logbook.txt"

#Write in the log file
logf = open(log_path,"a+")
logf.write("\n\n#### SCOPE LOGBOOK -- RUN NUMBER {} ####\n\n".format(runNumber))
logf.write("Date:\t{}\n".format(date))
logf.write("---------------------------------------------------------\n")
logf.write("Number of events per file: {} \n".format(numEvents))
logf.write("---------------------------------------------------------\n\n")

"""#################SCOPE HORIZONTAL SETUP#################"""
# dpo setup

dpo.write(':TIMebase:RANGe {}'.format(hScale)) ## Sets the full-scale horizontal time in s. Range value is ten times the time-per division value.
# # TIMebase:SCALe
dpo.write(':TIMebase:POSition 25E-9') ## offset
dpo.write(':ACQuire:MODE SEGMented') ## fast frame/segmented acquisition mode
dpo.write(':ACQuire:SEGMented:COUNt {}'.format(numEvents)) ##number of segments to acquire
dpo.write(':ACQuire:POINts:ANALog 6000')

print("# SCOPE HORIZONTAL SETUP #")
print('Horizontal scale set to {} for division\n'.format(hScale))

logf.write("HORIZONTAL SETUP\n")
logf.write('- Horizontal scale set to {} s for division\n\n'.format(hScale))

"""#################SCOPE CHANNELS BANDWIDTH#################"""
# dpo.write(':ACQuire:BANDwidth MAX') ## set the bandwidth to maximum
dpo.write('CHANnel1:ISIM:BANDwidth 2.00E+09')
dpo.write('CHANnel2:ISIM:BANDwidth 4.00E+09')
dpo.write('CHANnel3:ISIM:BANDwidth 3.50E+09')
dpo.write('CHANnel4:ISIM:BANDwidth 2.00E+09')
"""#################SCOPE VERTICAL SETUP#################"""
#vScale expressed in Volts
dpo.write('CHANnel1:SCALe {}'.format(vScale_ch1))
dpo.write('CHANnel2:SCALe {}'.format(vScale_ch2))
dpo.write('CHANnel3:SCALe {}'.format(vScale_ch3))
dpo.write('CHANnel4:SCALe {}'.format(vScale_ch4))

logf.write("VERTICAL SETUP\n")
logf.write('- CH1: vertical scale set to {} V for division\n'.format(vScale_ch1))
logf.write('- CH2: vertical scale set to {} V for division\n'.format(vScale_ch2))
logf.write('- CH3: vertical scale set to {} V for division\n'.format(vScale_ch3))
logf.write('- CH4: vertical scale set to {} V for division\n\n'.format(vScale_ch4))


"""#################TRIGGER SETUP#################"""
dpo.write('TRIGger:MODE EDGE; :TRIGger:EDGE:SOURce %s; :TRIGger:LEVel %s, %f'%(trigCh, trigCh, trigLevel))
dpo.write(':TRIGger:EDGE:SLOPe %s;' %(triggerSlope))

trigprint='%.3f'%(trigLevel)
print("# TRIGGER SETUP #")
print('Trigger scale set to %s V\n'%(trigprint))

logf.write("TRIGGER SETUP\n")
logf.write('- Trigger Channel set to %s\n'%(trigCh))
logf.write('- Trigger scale set to %s V\n\n\n\n'%(trigprint))

print('Horizontal, vertical, and trigger settings configured.\n')

"""#################DATA TRANSFERRING#################"""
# configure data transfer settings
dpo.write(':DIGitize')
# dpo.write(':RUN')
print(dpo.query('*OPC?'))
dpo.write(':DISK:SEGMented ALL') ##save all segments (as opposed to just the current segment)
print(dpo.query('*OPC?'))
dpo.write(':DISK:SAVE:WAVeform CHANnel1 ,"C:\\Users\\Public\\Documents\\AgilentWaveform\\Wavenewscope_CH1_21March_131kseg_test",H5,ON')
dpo.write(':DISK:SAVE:WAVeform CHANnel2 ,"C:\\Users\\Public\\Documents\\AgilentWaveform\\Wavenewscope_CH2_21March_131kseg_test",H5,ON')
dpo.write(':DISK:SAVE:WAVeform CHANnel3 ,"C:\\Users\\Public\\Documents\\AgilentWaveform\\Wavenewscope_CH3_21March_131kseg_test",H5,ON')
dpo.write(':DISK:SAVE:WAVeform CHANnel4 ,"C:\\Users\\Public\\Documents\\AgilentWaveform\\Wavenewscope_CH4_21March_131kseg_test",H5,ON')

dpo.close()
