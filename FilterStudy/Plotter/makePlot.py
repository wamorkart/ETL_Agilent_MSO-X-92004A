import ROOT
from ROOT import *
from plotterTools import *
import math
from array import array
import argparse

parser =  argparse.ArgumentParser(description='ETL Filter Study')
parser.add_argument('-s', '--sensor', dest='sensor', required=True, type=str)
parser.add_argument('-c', '--cfdLGAD', dest='cfdLGAD', required=True, type=str)

opt = parser.parse_args()
sensor = opt.sensor
cfd_lgad = opt.cfdLGAD

runs = []
if sensor == 'Pre-rad_UCSC_160':
    runs = runs_1

outputLoc = '/uscms/homes/t/twamorka/work/FilterStudy/Plotter/Filter_Plots/'

sigma_arr, sigma_err_arr = array( 'd' ), array( 'd' )
baselineRMS_arr, baselineRMS_err_arr = array( 'd' ), array( 'd' )
slewrate_arr, slewrate_err_arr = array( 'd' ), array( 'd' )
freq_arr, freq_err_arr = array( 'd' ), array( 'd' )
risetime_arr, risetime_err_arr = array( 'd' ), array( 'd' )
mpv,mpv_err = array('d'),array('d')
min_cfdLGAD = array('d')
## cfd scan for photek
nfreq = len(freq)
for f in freq:
    ch = TChain('pulse')
    for run in runs:
        for r in run:
            ch.Add('root://cmseos.fnal.gov//store/user/twamorka/FilterStudy/dat2Root_Filter/run_scope_dat2root_'+str(r)+'_'+str(f)+'.root')
    timePhotek_res = []
    timePhotek_res_err = []
    timeLGAD_res = []
    timeLGAD_res_err = []
    cfd_arr = []
    cfd_err_arr = []
    min_photek_cfd = 0
    min_lgad_cfd = 0
    for c in cfd:
        hname_photek = str(f)+'_'+str(c)
        h_photek = TH1F(hname_photek,hname_photek,100,-4e-9,-2e-9)
        ch.Draw('LP2_'+str(cfd_lgad)+'[0] - LP2_'+str(c)+'[3]>>' +hname_photek,TCut('LP2_'+str(cfd_lgad)+'[0]!=0&&LP2_'+str(c)+'[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
        c0 = TCanvas('c0','c0',800,600)
        gausFit = h_photek.Fit('gaus','S')
        timePhotek_res.append((gausFit.Parameters()[2])/1e-12)
        timePhotek_res_err.append((gausFit.Errors()[2])/1e-12)
        cfd_arr.append(c)
        cfd_err_arr.append(0)
        h_photek.Draw()
        c0.SaveAs(outputLoc+'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_Photekcfd_'+str(c)+'.pdf')
    npoints = len(cfd_arr)
    MakeGraphErrors(npoints,array('d',cfd_arr),array('d',timePhotek_res),array('d',cfd_err_arr),array('d',timePhotek_res_err),'CFD','Time Resolution [ps]',outputLoc,'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_vs_Photekcfd'+str(sensor)+'.pdf')
    min_photek_cfd = cfd_arr[min(xrange(len(timePhotek_res)), key=timePhotek_res.__getitem__)]
## cfd scan for LGAD
    for c in cfd:
        hname_lgad = str(f)+'_2_'+str(c)
        h_lgad = TH1F(hname_lgad,hname_lgad,100,-4e-9,-2e-9)
        ch.Draw('LP2_'+str(c)+'[0] - LP2_'+str(min_photek_cfd)+'[3]>>' +hname_lgad,TCut('LP2_'+str(c)+'[0]!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
        gausFit2 = h_lgad.Fit('gaus','S')
        timeLGAD_res.append((gausFit2.Parameters()[2])/1e-12)
        timeLGAD_res_err.append((gausFit2.Errors()[2])/1e-12)
        h_lgad.Draw()
        c0.SaveAs(outputLoc+'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_LGADcfd_'+str(c)+'.pdf')
    min_lgad_cfd = cfd_arr[min(xrange(len(timeLGAD_res)), key=timeLGAD_res.__getitem__)]
    min_cfdLGAD.append(min_lgad_cfd)
    MakeGraphErrors(npoints,array('d',cfd_arr),array('d',timeLGAD_res),array('d',cfd_err_arr),array('d',timeLGAD_res_err),'CFD','Time Resolution [ps]',outputLoc,'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_vs_LGADcfd'+str(sensor)+'.pdf')

    hname = 'dummy_hist'
    print "min lgad cfd ", min_lgad_cfd
    h1 = TH1F(hname,hname,100,-2.8e-9,-1.8e-9)
    ch.Draw('LP2_'+str(min_lgad_cfd)+'[0] - LP2_30[3] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'[0]!=0&&LP2_30[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
    c = TCanvas('c','c',800,600)
    gausFit = h1.Fit('gaus','S')
    h1.Draw()
    c.SaveAs('freq_'+str(f)+'.pdf')
    sigma_arr.append((gausFit.Parameters()[2])/1e-12)
    sigma_err_arr.append((gausFit.Errors()[2])/1e-12)
    freq_arr.append(f)
    freq_err_arr.append(0)

    h2 = TH1F(hname,hname,100,0,100)
    ch.Draw('baseline_RMS[0] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'[0]!=0&&LP2_30[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
    baselineRMS_arr.append(h2.GetMean())
    baselineRMS_err_arr.append(h2.GetMeanError())

    h3 = TH1F(hname,hname,100,-3000,100)
    ch.Draw('risetime[0]/1e9 >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'[0]!=0&&LP2_30[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
    slewrate_arr.append(abs(h3.GetMean()))
    slewrate_err_arr.append(abs(h3.GetMeanError()))

    h4 = TH1F(hname,hname,100,0,200)
    ch.Draw('amp[0] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'[0]!=0&&LP2_30[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
    lanFit = h4.Fit('landau','S')
    h4.Draw()
    c.SaveAs('freq_mpv'+str(f)+'.pdf')
    mpv.append(lanFit.Parameters()[1])
    mpv_err.append(lanFit.Errors()[1])

    h5 = TH1F(hname,hname,100,-100,100)
    ch.Draw('amp[0]*1e9/risetime[0] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'[0]!=0&&LP2_30[3]!=0&&amp[0]>30&&amp[3]>100&&amp[3]<200'))
    risetime_arr.append(abs(h5.GetMean()))
    risetime_err_arr.append(abs(h5.GetMeanError()))


jitter = [float(ai)/bi for ai,bi in zip(baselineRMS_arr,slewrate_arr)]
mpv_over_noise = [float(ai)/bi for ai,bi in zip(mpv,baselineRMS_arr)]

MakeGraphErrors(nfreq,freq_arr,sigma_arr,freq_err_arr,sigma_err_arr,'Filter Frequency [MHz]','Time Resolution [ps]',outputLoc,'TimRes_vs_Freq_'+str(sensor)+'.pdf')
MakeGraphErrors(nfreq,freq_arr,baselineRMS_arr,freq_err_arr,baselineRMS_err_arr,'Filter Frequency [MHz]','Baseline RMS',outputLoc,'BaselineRMS_vs_Freq_'+str(sensor)+'.pdf')
MakeGraphErrors(nfreq,freq_arr,slewrate_arr,freq_err_arr,slewrate_err_arr,'Filter Frequency [MHz]','Slew Rate (dV/dt)',outputLoc,'dVdT_vs_Freq_'+str(sensor)+'.pdf')
MakeGraphErrors(nfreq,freq_arr,mpv,freq_err_arr,mpv_err,'Filter Frequency [MHz]','Amplitude [mV]',outputLoc,'Amp_vs_Freq_'+str(sensor)+'.pdf')
MakeGraphErrors(nfreq,freq_arr,risetime_arr,freq_err_arr,risetime_err_arr,'Filter Frequency [MHz]','Rise time [ns]',outputLoc,'Risetime_vs_Freq_'+str(sensor)+'.pdf')
MakeGraph(nfreq,freq_arr,array('d',jitter),'Filter Frequency [MHz]','Jitter [ns]',outputLoc,'Jitter_vs_Freq_'+str(sensor)+'.pdf')
MakeGraph(nfreq,freq_arr,min_cfdLGAD,'Filter Frequency [MHz]','Min. LGAD cfd',outputLoc,'MinLGAD_vs_Freq_'+str(sensor)+'.pdf')
MakeGraph(nfreq,freq_arr,array('d',mpv_over_noise),'Filter Frequency [MHz]','MPV/Baseline RMS',outputLoc,'MPVoverNoise_Freq_'+str(sensor)+'.pdf')
