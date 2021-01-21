#!/bin/bash

basedir=/asl/models/era5_avg
srcdir=${basedir}/INCOMING

for file in $(find $srcdir -size +3G -name "*_lev.nc"); do
    # assumes that corresponding surface download, which happens
    # first, completed successfully
    ym=$(basename $file .nc)
    year=${ym:0:4}
    
    if [[ ! -d ${basedir}/$year ]]; then
	echo "Year directory $year does not exist. Creating."
	mkdir -p ${basedir}/${year}
    fi

    echo "Compressing $ym and corresponding surface file"
    # compress levels file
    nccopy -u -d9 $file ${basedir}/${year}/${ym}.nc
    mv $file ${file}.1
    # compress corresponding surface file
    nccopy -u -d9 ${file/lev/sfc} ${basedir}/${year}/${ym/lev/sfc}.nc
    mv ${file/lev/sfc} ${file/lev/sfc}.1

done
