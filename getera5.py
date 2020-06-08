#!/usr/bin/env python

# Grab a period of days of ECMWF ERA5 data with a subset of variables
# useful to UMBC ASL

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

scratch_dir = "/umbc/hpcnfs1/strow/asl/data/era5/INCOMING"
if os.path.exists(scratch_dir) is False:
    os.mkdir(scratch_dir)
    
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

requestDates = StartDate + "/TO/" + EndDate

targetBase = '%08s-%08s' % (StartDate_string, EndDate_string)

# use of cdsapi requires a user account and download key with ECMWF
# CDS (https://cds.climate.copernicus.eu/) which gets stored locally
# in the file ~/.cdsapirc

cds = cdsapi.Client()

# select times to bring down. ERA/ECMWF is/was 6-hourly and prior work
# brought down 0,6,12,18 hours. ERA5 offers hourly resolution
times = '00/to/23/by/3'  # 0,3,6,9,12,15,18,21
grid = '0.25/0.25'    # '0.25/0.25'  - ERA5 full | '0.75/0.75'  - ERA-Interim

levtype = "ml"        # model levels (how to specify the 60 level version?)
levels = '1/to/137'
plist = ['130',  # temperature
         '133',  # specific humidity
         '203',  # ozone mass mixing ratio
         '246',  # specific cloud liquid water content
         '247',  # specific cloud ice water content
         '248']  # fraction of cloud cover

target = '%s-sfc.nc' % (targetBase)

######
# FUNCTION DEFS
######
def getera5_level_var(requestDates, param, target):

    cds.retrieve('reanalysis-era5-complete', {
        'class': 'ea',
        'date': requestDates,
        'grid': grid,
        'expver': '0001',    # 5 for dates within 3 months of present?
        'levelist': levels,
        'levtype': levtype,
        'param': param,
        'stream': 'oper',
        'time': times,
        'type': 'an',
        #'product_type': 'reanalysis',
        'format': 'netcdf'
    }, target )


def getera5_surf_params(requestDates, target):
    # surface parameters
    levtype = 'sfc'
    # params = '31.128/134.128/164.128/165.128/166.128/235.128'
    vlist = ['sea_ice_cover',
             'surface_pressure',
             'total_cloud_cover',
             '10m_u_component_of_wind',
             '10m_v_component_of_wind',
             'skin_temperature']
    cds.retrieve('reanalysis-era5-single-levels', {
        'class': 'ea',
        'date': requestDates,
        'grid': grid,
        'expver': '0001',
        'levtype': levtype,
        'variable': vlist,
        'stream': 'oper',
        'time': times,
        'product_type': 'reanalysis',
        'format': 'netcdf'
    }, target )
#######
# END FUNCTION DEFS
#######

#print(">> Retrieving surface data for", requestDates, sep=":", flush="true")
#getera5_surf_params(requestDates, target)

for param in plist:
    print(">> Retrieving level data for", requestDates, param, sep=":", flush="true")
    target = '%s-lev-%s.nc' % (targetBase, param)
    getera5_level_var(requestDates, param, target)

