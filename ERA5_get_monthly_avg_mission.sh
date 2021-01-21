#!/bin/bash

# put ourselves into reception directory
#cd /asl/models/era5_avg/INCOMING

driver_file_sorted=era5_monthly.driver
driver_file=${driver_file_sorted}.shuffled

# build driver file of year/months to download (already have 2018)
echo "> Build driver file for download..."
for month in {08..12}; do
    echo "2002 $month" >> $driver_file_sorted
done

for year in {2003..2017} {2019..2020}; do
    for month in {01..12}; do
	echo "$year $month" >> $driver_file_sorted
    done
done

# shuffle driver file for interleaved download
shuf --output=$driver_file $driver_file_sorted
echo "> Download driver complete. Starting downloads."

# read through driver file and download year/month combinations
while IFS= read -r line
do
    # parse year and month
    year=${line:0:4}
    month=${line:5:2}

    # run ERA5_get_monthly_avg.py
    echo ">> Run download for $year/$month..."
    ERA5_get_monthly_avg.py ERA5.ini $year $month >> logfile 2>&1

done < "$driver_file"

    
