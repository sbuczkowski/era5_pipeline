#!/usr/bin/env python

# Grab a day of ECMWF ERA5/ERA5T surface temp data 

# ECMWF Climate Data Store CDS API
import cdsapi
import sys
import os

sys.path.append('/home/sbuczko1/git/era5_pipeline/')

if len (sys.argv) != 3:
    print(" Please specify two dates for range (eg: 20140729 20140730  for two days)")
    sys.exit(1)

    
if len(sys.argv[1]) != 8:
    print("  Please specify a date YYYYMMDD (eg: 20140729)")
    sys.exit(1)
if len(sys.argv[2]) != 8:
    print("  Please specify a date YYYYMMDD (eg: 20140729)")
    sys.exit(1)
    
StartDate_string = sys.argv[1]
StartYear = StartDate_string[0:4]
StartMonth = StartDate_string[4:6]
StartDay = StartDate_string[6:8]
StartDate = '%04s%02s%02s' % (StartYear, StartMonth, StartDay)    

EndDate_string = sys.argv[2]
EndYear = EndDate_string[0:4]
EndMonth = EndDate_string[4:6]
EndDay = EndDate_string[6:8]
EndDate = '%04s%02s%02s' % (EndYear, EndMonth, EndDay)    

date_string = StartDate + "/TO/" + EndDate
date_short = StartYear + StartMonth + StartDay + "-" + EndDay


scratch_dir = os.path.join("/umbc/hpcnfs1/strow/asl/data/era5",StartYear,StartMonth)
if os.path.exists(scratch_dir) is False:
    os.mkdir(scratch_dir)

# use of cdsapi requires a user account and download key with ECMWF
# CDS (https://cds.climate.copernicus.eu/) which gets stored locally
# in the file ~/.cdsapirc

cds = cdsapi.Client()

output_format = 'netcdf' # grib/netcdf (netcdf is 64-bit offset, uncompressed)

# select times to bring down. ERA/ECMWF is/was 6-hourly and prior work
# brought down 0,6,12,18 hours. ERA5 offers hourly resolution
times = '00/to/23/by/3'  # 0,3,6,9,12,15,18,21
grid = '0.25/0.25'    # '0.25/0.25'  - ERA5 full | '0.75/0.75'  - ERA-Interim
vlist = ['temperature',
         'specific_humidity',
         'ozone_mass_mixing_ratio',
         'specific_cloud_liquid_water_content',
         'specific_cloud_ice_water_content',
         'fraction_of_cloud_cover']
plist = ['130',
         '133',
         '203',
         '246',
         '247',
         '248']

# surface parameters
fn = scratch_dir + "/" + date_short + "_test.nc"
levtype = 'ml'
levels = '1/to/137'

cds.retrieve('reanalysis-era5-complete', {
    'class': 'ea',
    'date': date_string,
    'grid': grid,
    'expver': '0001',
    'levelist' : levels,
    'levtype': levtype,
#    'variable': vlist[0],
#    'param' : 130/133/203/246/247/248,
    'param' : plist[0],
    'stream': 'oper',
    'time': times,
#    'product_type': 'reanalysis',
    'type': 'an',
    'format': 'netcdf'
}, fn )
