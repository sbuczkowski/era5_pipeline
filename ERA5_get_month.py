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

scratch_dir = "/umbc/isilon/rs/strow/asl/ERA5/INCOMING"
if os.path.exists(scratch_dir) is False:
    os.mkdir(scratch_dir)
    
year = int(sys.argv[2])
month = int(sys.argv[3])
baseDateStr = "%04d%02d" % (year, month)

######
# surface variable pull
######
requestDates = []
(i,ndays) = calendar.monthrange(year, month)
for i in range(ndays):
    requestDates.append(baseDateStr + "{day:02}".format(day=i+1))

StartDate = baseDateStr + "{day:02}".format(day=1) 
EndDate = baseDateStr + "{day:02}".format(day=ndays) 
target = os.path.join(scratch_dir, '%s-%s_sfc.nc' % (StartDate, EndDate))
print(StartDate, EndDate, target)

ERA5Queries.get_surf_params(cds, requestDates, target, config)
######
# End surface variable pull
######

######
# levels variable pulls
######
requestDates = []
(i,ndays) = calendar.monthrange(year, month)
requestDates.append(baseDateStr + "{day:02}".format(day=1) + '/to/' + baseDateStr + "{day:02}".format(day=12))
requestDates.append(baseDateStr + "{day:02}".format(day=13) + '/to/' + baseDateStr + "{day:02}".format(day=24))
requestDates.append(baseDateStr + "{day:02}".format(day=25) + '/to/' + baseDateStr + "{day:02}".format(day=ndays))

plist = ['130',
         '133',
         '203',
         '246',
         '247',
         '248']

for i in range(len(requestDates)):
    for j in range(len(plist)):
        target = os.path.join(scratch_dir, \
                              requestDates[i].replace('/to/','-') + \
                              "_lev_{pval:03}".format(pval=int(plist[j])) + ".nc")
        print(target)
        ERA5Queries.get_level_param(cds, requestDates[i], plist[j], target, config)

######
# End levels variable pulls
######

