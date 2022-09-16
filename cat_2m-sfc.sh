#!/bin/bash

mdir=/asl/models/era5_avg/INCOMING
era5dir=/asl/models/era5_avg

cd $mdir

for mfile in $(ls *_2m.nc); do
	tdate=${mfile:0:7}
	year=${mfile:0:4}
	erafile=${era5dir}/${year}/${tdate}_sfc.nc
	
	if [[ ! -f $erafile ]]; then
		echo "ERA5 file $erafile does not exist"
		continue
	fi

	ncks -A $mfile $erafile

done
