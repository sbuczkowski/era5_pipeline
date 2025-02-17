#!/usr/bin/env python

# Grab a period of days of ECMWF ERA5 data with a subset of variables
# useful to UMBC ASL

# ECMWF Climate Data Store CDS API
import cdsapi
import sys
import os
import calendar
import ERA5Queries
import configparser

sys.path.append('/home/sbuczko1/git/era5_pipeline/')

if len (sys.argv) != 4:
    print(" Please specify config file, year, and month to retrieve (ini YYYY MM)")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(sys.argv[1])

scratch_dir = "/umbc/isilon/rs/strow/asl/ERA5/INCOMING"
if os.path.exists(scratch_dir) is False:
    os.mkdir(scratch_dir)
    
year = int(sys.argv[2])
month = int(sys.argv[3])
baseDateStr = "%04d%02d" % (year, month)

requestDates = []
(i,ndays) = calendar.monthrange(year, month)
for i in range(ndays):
    requestDates.append(baseDateStr + "{day:02}".format(day=i+1))

print(requestDates)

StartDate = baseDateStr + "{day:02}".format(day=1) 
EndDate = baseDateStr + "{day:02}".format(day=ndays) 
target = os.path.join(scratch_dir, '%s-%s_sfc.nc' % (StartDate, EndDate))
print(StartDate, EndDate, target)

# use of cdsapi requires a user account and download key with ECMWF
# CDS (https://cds.climate.copernicus.eu/) which gets stored locally
# in the file ~/.cdsapirc

cds = cdsapi.Client()

# select times to bring down. ERA/ECMWF is/was 6-hourly and prior work
# brought down 0,6,12,18 hours. ERA5 offers hourly resolution

ERA5Queries.get_surf_params(cds, requestDates, target, config)

