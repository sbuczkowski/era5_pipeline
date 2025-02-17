#!/bin/bash

# ERA5 levels parameter files are downloaded as a single file for each
# levels variable covering a 12 day period. A month will consist of
# three separate filesets with two covering the first 24 days of the
# month and the third bringing in the remaining days.  Those filesets
# need to be broken out into separate daily files containing all
# parameters by splitting each N-day variable file into N variable
# files and concatenating into N daily files containing all variables.

# files are downloaded with the naming convention
# STARTDATE-ENDDATE_lev_{paramid}.nc and need to be broken out into files as
# STARTDATE_lev_{paramid}.nc
# (STARTDATE + 1 day)_lev_{paramid}.nc
# ...
# (ENDDATE - 1 day)_lev_{paramid}.nc
# ENDDATE_lev_{paramid}.nc
#
# and subsequently concatenated into corresponding daily files
# e.g. STARTDATE_lev.nc

# requires NCO (module load NCO/4.7.6-intel-2018a) (should check for
# loaded existence and load, if necessary)

# filenames to process look like 20190101-20190112_lev_{paramid}.nc
# script takes in the date range portion 
# e.g. splitcat_lev_files 20190101-20190112 
# 
# and can be run on multiple ranges in a loop like:
# for i in $(ls *_lev_*.nc | cut -d_ -f1 | sort -n | uniq); do 
#     splitcat_lev_files $i
# done
fnamebase=$1

# establish canonical processing directory trees
BASEDIR="/umbc/isilon/rs/strow/asl/ERA5"
INCDIR=${BASEDIR}/INCOMING
TEMPDIR=${INCDIR}/LEV_TEMP

varlist=(t q o3 clwc ciwc cc)
varidlist=(130 133 203 246 247 248)

echo "Procesing ERA5 levels file split/append for date range file $fnamebase"
echo $(date)

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
    echo "> Processing ${darray[$i]}"
    tindexstart=$(($i * $ntsteps))
    tindexend=$(( (($i + 1) * $ntsteps - 1) ))
    YEAR=${darray[$i]:0:4}
    MONTH=${darray[$i]:4:2}

    # pull out first var (t) and use to establish output file. Will
    # concatenate further variables into this
    fname=${ifilebase}_lev_${varidlist[0]}.nc
    ofile=$TEMPDIR/TEMP_${darray[$i]}_lev_${varlist[0]}.nc
    dname=${darray[$i]}_lev.nc
    tdfile=$TEMPDIR/TEMP_$dname
    echo -n ">> Extracting ${varlist[0]} data to $ofile"
    ncks --overwrite -d time,${tindexstart},${tindexend} $fname $ofile
    echo " ... Moving $ofile to $tdfile to start appends."
    cp $ofile $tdfile
    for j in $(seq 1 $(( ${#varlist[@]} - 1 )) ); do
	fname=${ifilebase}_lev_${varidlist[$j]}.nc
	ofile=$TEMPDIR/TEMP_${darray[$i]}_lev_${varlist[$j]}.nc
	echo -n ">> Extracting ${varlist[$j]} data to $ofile"
	ncks --overwrite -d time,${tindexstart},${tindexend} $fname $ofile

	# append current variable into daily file
	echo " ... Appending to $tdfile"
	ncks -A $ofile $tdfile
    done

    # post-processing and clean up
    OUTPUTBASE=$BASEDIR/$YEAR/$MONTH
    dfile=$OUTPUTBASE/$dname
    echo ">> Moving $tdfile to $dfile"
    if [[ ! -d $OUTPUTBASE ]]; then
	echo ">>> $OUTPUTBASE does note exist. Creating."
	mkdir -p $OUTPUTBASE
    fi
    mv $tdfile $dfile

    # remove TEMP_* files
    echo ">> Removing temporary files"
    # rm $TEMPDIR/TEMP_*.nc

done
echo "Procesing levels file split/append for $fnamebase complete"
echo $(date)
