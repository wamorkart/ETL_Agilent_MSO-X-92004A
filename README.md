# ETL_Agilent_MSO-X-92004A
Data acquisition and reconstruction for the Agilent MSO-X-92004A ocsilloscope.
This is based on the Tektronix repository https://github.com/tommasoisi/Tektronix_DPO7254Control

Instructions for the acquisition and reconstruction part are here:

## Acquisition
This step produces files in the HDF5 format
## Reconstruction
The files created with the previous step are converted into ROOT TTree's using the h5py python package. This step requires the .h5 files for the 4 channels as input.
### How to run?
* Acquisition
`python acquisition.py --numEvents 20000 --trigCh 2 --trig -0.05`
* Conversion
First make sure you have the h5py package. If you have an existing python installation, do
`pip install h5py`
Run the conversion script
`python conversion_h5.py --inputFiles 1 2 3 4`
