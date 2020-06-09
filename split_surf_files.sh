#!/bin/bash

# ERA5 surface parameter files are downloaded as a single file
# covering an entire month. Those files need to be broken out into
# separate daily files containing all parameters

# files are downloaded with the naming convention
# STARTDATE-ENDDATE_sfc.nc and need to be broken out into files as
# STARTDATE_sfc.nc
# (STARTDATE + 1 day)_sfc.nc
# ...
# (ENDDATE - 1 day)_sfc.nc
# ENDDATE_sfc.nc

# requires NCO (module load NCO/4.7.6-intel-2018a)

fname=$1

BASEDIR="/umbc/isilon/rs/strow/asl/ERA5"

# extract start and end dates from filename
declare -a drange=()
IFS='-' read -r -a drange <<< $(basename $fname _sfc.nc)

# generate YYYYMMDD date strings for dates between start and end date
# inclusive
declare -a darray=(); 
for dt in $(seq -w ${drange[0]} ${drange[1]}) ; do 
    darray+=($(date -d $dt +'%Y%m%d')) 2> /dev/null
done 

# loop over dates within the file and generate YYYYMMDD date strings
# for dates between start and end date
# currentday=${drange[0]}
# while ! [[ $currentday > ${drange[1]} ]]; do
#     echo "> Extracting and processing $currentday"
    
#     ncks -v time,$starttime,$endtime $fname ${currentday}_sfc.nc



#     currentday=$(date -d "$currentday + 1 day" +"%Y%m%d")
# done

# loop over dates in file
ntsteps=8
for i in ${!darray[@]}; do
    tindexstart=$(($i * $ntsteps))
    tindexend=$(( (($i + 1) * $ntsteps - 1) ))
    YEAR=${darray[$i]:0:4}
    MONTH=${darray[$i]:4:2}
#    echo "$BASEDIR/$YEAR/$MONTH/${darray[$i]}_sfc.nc"
    ncks -d time,${tindexstart},${tindexend} $fname $BASEDIR/$YEAR/$MONTH/${darray[$i]}_sfc.nc

done
