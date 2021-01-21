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

# filenames to process look like 20190101-20190112_sfc.nc
# script takes in the date range portion 
# e.g. split_surf_files 20190101-20190112 
# 
# and can be run on multiple ranges in a loop like:
# for i in $(ls *_sfc.nc | cut -d_ -f1 | sort -n | uniq); do 
#     split_surf_files $i
# done
fnamebase=$1

# establish canonical processing directory trees
BASEDIR="/umbc/isilon/rs/strow/asl/ERA5"
INCDIR=${BASEDIR}/INCOMING
TEMPDIR=${INCDIR}/SFC_TEMP

echo "Procesing ERA5 surface file split for $fnamebase"
echo $(date)

fname=${fnamebase}_sfc.nc

# extract start and end dates from filename
declare -a drange=()
IFS='-' read -r -a drange <<< $(echo $fnamebase)
ifilebase=${drange[0]}-${drange[1]}
if [ "$fnamebase" != "$ifilebase" ]; then
    echo "**!> ERROR: extracted date range does not match input. EXITING. <!**"
    exit
fi

# generate YYYYMMDD date strings for dates between start and end date
# inclusive
declare -a darray=(); 
for dt in $(seq -w ${drange[0]} ${drange[1]}) ; do 
    darray+=($(date -d $dt +'%Y%m%d')) 2> /dev/null
done 
echo "> Found ${#darray[*]} dates to process within file range"

# loop over dates in file
ntsteps=8
for i in ${!darray[@]}; do
    tindexstart=$(($i * $ntsteps))
    tindexend=$(( (($i + 1) * $ntsteps - 1) ))
    YEAR=${darray[$i]:0:4}
    MONTH=${darray[$i]:4:2}
    dname=${darray[$i]}_sfc.nc
    tdfile=${TEMPDIR}/TEMP_${dname}

    echo ">> $fnamebase -> $outfile"
    ncks -d time,${tindexstart},${tindexend} $fname $tdfile

    OUTPUTBASE=$BASEDIR/$YEAR/$MONTH
    dfile=${OUTPUTBASE}/${dname}
    echo ">> Moving $tdfile to $dfile"
    if [[ ! -d $OUTPUTBASE ]]; then
	echo ">>> $OUTPUTBASE does not exist. Creating."
	mkdir -p $OUTPUTBASE
    fi
    mv $tdfile $dfile

    # remove TEMP_* files
    echo ">> Removing temporary files"
    # rm $TEMPDIR/TEMP_*.nc

done
echo "Processing surface file split for $fnamebase complete"
echo $(date)

