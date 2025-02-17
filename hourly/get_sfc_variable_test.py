#!/usr/bin/env python

# Grab a period of days of ECMWF ERA5 data with a subset of variables
# useful to UMBC ASL

# ECMWF Climate Data Store CDS API
import cdsapi

cds = cdsapi.Client()

requestDates = "20210101"
target = "/home/sbuczko1/Work/era5_test-2.nc"

vlist = ['2m_temperature',
         '2m_dewpoint_temperature']

cds.retrieve('reanalysis-era5-single-levels', {
    'class': 'ea',
    'date': requestDates,
    'grid': '0.25/0.25',
    'expver': '0001',
    'levtype': 'sfc',
    'variable': vlist,
    'stream': 'oper',
    'time': "00/to/23/by/6",
    'product_type': 'reanalysis',
    'format': 'netcdf'
}, target )
