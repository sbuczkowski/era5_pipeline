#!/bin/bash

# use nccopy to compress era5 files 

# era5 files do not appear to have any UNLIMITED dimensions but run
# nccopy with '-u' anyway, just in case. Go straight to '-d9'
# compression level

# routine takes in path and basefilename for a set of netcdf files as
# produced by the era5 pipeline

# e.g. for downloaded and separated ERA5 netcdf files
# conversion produces 2 files in the same tree: YYYYMMDD_{sfc,lev}.nc
# This routine compresses each of those netcdf files through nccopy

# check for verbose output flag
while getopts vf: flag
do
    case "${flag}" in
	v) verbose=1;;
	f) ncfilebase=${OPTARG};;
	*) echo -e "Usage: compress_era5 (-v) -f filebasepath\n"
	    exit
	    ;;
    esac
done

# make sure netcdf tools are loaded
module try-load NCO/4.7.6-intel-2018a

#ncfilebase=$1
echo "NCFILEBASE = $ncfilebase"

declare -a fsuffix=(sfc lev)
declare -a sfilesize=(80000000 6000000000)

for index in ${!fsuffix[*]}; do
    ftype=${fsuffix[$index]}
    fsize=${sfilesize[$index]}
    
    ncfile=${ncfilebase}_${ftype}.nc
    tncfile=${ncfile}.compressed
    filesize=$(stat -c%s $ncfile)
    
    if [[ ! -f $tncfile && $filesize -gt $fsize ]]; then
	test $verbose && echo ">>> Compressing $ncfile: nccopy -u -d9 $ncfile ${tncfile}"
	nccopy -u -d9 $ncfile ${tncfile}
    fi

    # Second if-then block to move compressed files into place
    # even if they were just created above
    if [[ -f $tncfile ]]; then
	test $verbose && echo ">>> $tncfile exists, moving to replace $ncfile: mv $tncfile $ncfile"
	mv $tncfile $ncfile
    else
	test $verbose &&echo ">>> $ncfile already compressed and replaced"
    fi

done

