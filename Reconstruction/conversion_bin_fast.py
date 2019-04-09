import struct  #struct unpack result - tuple
import numpy as np
import matplotlib.pyplot as plt
import ROOT
from ROOT import *
import time
import optparse
import argparse

parser = argparse.ArgumentParser(description='Reconstruction')

parser.add_argument('--inputFiles', metavar='input', type=str, nargs = '+', help='input files from 4 channels',required=True)
args = parser.parse_args()



def fast_Keysight_bin(filepath_in, index_in):
    global x_axis, y_axis, remaining
    x_axis = []
    y_axis = []

    # read from file
    my_index = index_in
    # start = time.time()
    my_file = open(filepath_in, 'rb')

    b_cookie = my_file.read(2) #char
    b_version = my_file.read(2) #char
    b_size = struct.unpack('i', my_file.read(4)) #int32 - i
    b_nwaveforms = struct.unpack('i', my_file.read(4)) #int32 - i ## number of events (or segments)
    # end = time.time()

    if my_index <= b_nwaveforms[0]:
        my_index = my_index
    else:
        my_index = 1
    counter = 0

    nBytesPerEvent = 16152 ##-- 140+12+16000
    my_file.seek( (nBytesPerEvent)*(my_index-1) ,1)
    b_header = struct.unpack('i', my_file.read(4)) #int32 - i
    # print " b_header = ", (b_header)
    remaining = b_header[0] - 4
    # print " remaining = ", remaining
    b_wavetype = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_wavebuffers = struct.unpack('i', my_file.read(4)) #int32 - i
    # print " b_wavebuffers = ", (b_wavebuffers[0])
    remaining = remaining - 4
    b_points = struct.unpack('i', my_file.read(4)) #int32 - i
    # print " b_point =", (b_points)
    remaining = remaining - 4
    b_count = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_x_disp_range = struct.unpack('f', my_file.read(4)) #float32 - f
    remaining = remaining - 4
    b_x_disp_orig = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_x_inc = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_x_orig = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_x_units = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_y_units = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_date =  my_file.read(16)
    remaining = remaining - 16
    b_time =  my_file.read(16)
    remaining = remaining - 16
    b_frame =  my_file.read(24)
    remaining = remaining - 24
    b_wave_string =  my_file.read(16)
    remaining = remaining - 16
    b_time_tag = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_segment_index = struct.unpack('I', my_file.read(4)) #unsigned int - I
    remaining = remaining - 4
    # print " remaining is now = ", remaining

    x_axis = b_x_orig[0] + b_x_inc[0] * np.linspace(0, b_points[0]-1, b_points[0])

   # j loop on buffers - only returns the last buffer
    for j in range(0,b_wavebuffers[0]):
        counter += 1
        #header size - int 32
        b_header = struct.unpack('i' , my_file.read(4)) #int32 - i
        # print 'buffer header size: ' ,( str(b_header[0]))
        remaining = b_header[0] - 4
        #buffer type - int16
        b_buffer_type = struct.unpack('h' , my_file.read(2)) #int16 - h
        # print 'buffer type: ' ,( str(b_buffer_type[0]))
        remaining = remaining - 2
        #bytes per point - int16
        b_bytes_per_point = struct.unpack('h' , my_file.read(2)) #int16 - h
        # print 'bytes per point: ' ,( str(b_bytes_per_point[0]) )
        remaining = remaining - 2
        #buffer size - int32
        b_buffer_size = struct.unpack('i' , my_file.read(4)) #int32 - i
        # print 'buffer size: ' ,( str(b_buffer_size[0]) )
        remaining = remaining - 4
        # create y axis for voltage vector
        # currently ONLY standard voltage -  float32 - Buffer Type 1 / 2 / 3
        # print  " buffer size = ", (b_buffer_size[0])
        b_y_data = my_file.read(b_buffer_size[0])
        y_axis = struct.unpack("<"+str(b_points[0])+"f", b_y_data)
    return_array = [x_axis,y_axis]
    # print " counter = ", (counter)
    # print len(return_array[0])
    # print (return_array[1])
    return return_array, b_nwaveforms, b_points

## read the input files

inputFile1 = 'Wavenewscope_CH.bin'
inputFile2 = 'Wavenewscope_CH.bin'
inputFile3 = 'Wavenewscope_CH.bin'
inputFile4 = 'Wavenewscope_CH.bin'


inputFile1 = 'Wavenewscope_CH3_Apr2_87.bin'
inputFile2 = 'Wavenewscope_CH3_Apr2_87.bin'
inputFile3 = 'Wavenewscope_CH3_Apr2_87.bin'
inputFile4 = 'Wavenewscope_CH3_Apr2_87.bin'

## prepare the output files
outputFile = 'output_fastbin.root'
outRoot = TFile(outputFile, "RECREATE")
outTree = TTree("reco","reco")

i_evt = np.zeros(1,dtype=np.dtype("u4"))
channel = np.zeros([4,4000],dtype=np.float32)
time = np.zeros([1,4000],dtype=np.float32)

outTree.Branch('i_evt',i_evt,'i_evt/i')
outTree.Branch( 'channel', channel, 'channel[4][4000]/F' )
outTree.Branch( 'time', time, 'time[1][4000]/F')


input1 = fast_Keysight_bin(inputFile1,1)

n_events = list (input1[1])[0] ## number of events/segments
n_points = list(input1[2])[0] ## number of points acquired for each event/segment
print "n_events = ", n_events
print "n_points = ", n_points


voltage_CH1 = []
voltage_CH2 = []
voltage_CH3 = []
voltage_CH4 = []

for i in range(n_points):
    voltage_CH1.append(fast_Keysight_bin(inputFile1, i+1))
    voltage_CH2.append(fast_Keysight_bin(inputFile2, i+1))
    voltage_CH3.append(fast_Keysight_bin(inputFile3, i+1))
    voltage_CH4.append(fast_Keysight_bin(inputFile4, i+1))

channel[0] = voltage_CH1[0][0][1]
channel[1] = voltage_CH2[0][0][1]
channel[2] = voltage_CH3[0][0][1]
channel[3] = voltage_CH4[0][0][1]
time[0] = voltage_CH1[0][0][0]

for event in range(n_events):
    i_evt[0] = event
    outTree.Fill()

outRoot.cd()
outTree.Write()
outRoot.Close()
