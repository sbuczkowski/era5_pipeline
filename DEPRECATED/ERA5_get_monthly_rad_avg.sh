#!/bin/bash

# put ourselves into reception directory
#cd /asl/models/era5_avg/INCOMING

driver_file=$1

# read through driver file and download year/month combinations
while IFS= read -r line
do
    # parse year and month
    year=${line:0:4}
    month=${line:5:2}

    # run ERA5_get_monthly_rad_avg.py
    echo ">> Run download for $year/$month..."
    ERA5_get_monthly_rad_avg.py ERA5.ini $year $month >> logfile 2>&1

done < "$driver_file"

    
