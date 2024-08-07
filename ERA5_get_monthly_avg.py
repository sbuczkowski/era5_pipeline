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

# use of cdsapi requires a user account and download key with ECMWF
# CDS (https://cds.climate.copernicus.eu/) which gets stored locally
# in the file ~/.cdsapirc

cds = cdsapi.Client()

scratch_dir = "/asl/models/era5_monthly/INCOMING"
if os.path.exists(scratch_dir) is False:
    os.mkdir(scratch_dir)
    
year = int(sys.argv[2])
month = int(sys.argv[3])
baseDateStr = "%04d%02d" % (year, month)

######
# surface variable pull
######
target = os.path.join(scratch_dir, '%04d-%02d_sfc.nc' % (year, month))
print(baseDateStr, target)

ERA5Queries.get_surf_monthly_avg(cds, year, month, target, config)
######
# End surface variable pull
######

######
# levels variable pulls
######
target = os.path.join(scratch_dir, '%04d-%02d_lev.nc' % (year, month))
print(baseDateStr, target)

ERA5Queries.get_levels_monthly_avg(cds, year, month, target, config)

######
# End levels variable pulls
######

