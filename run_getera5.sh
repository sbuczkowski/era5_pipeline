#!/bin/bash
# run_getera5 <year> <startmonth> <endmonth>
# run_getera5 2019 1 4  : get Jan-Apr, 2019

year=$1
monthstart=$2
monthend=$3

for month in $(seq -f "%02g" $monthstart $monthend) ; do 
    lastday=$(date -d "${year}-${month}-01 - +1 month - 1 day" +"%d"); 
    for day in $(seq -f "%02g" 1 $lastday); do 
	getera5 ${year}${month}${day}
# now sleep before the next iteration (trying to avoid stressing the 
# CDS Copernicus server(s) into dropping and restarting the connection
	sleep 60
    done
done
