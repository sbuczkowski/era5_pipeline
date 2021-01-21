#!/bin/bash

#SBATCH --job-name=COMPRESS_ERA5
#SBATCH --partition=batch
#SBATCH --qos=short+
#SBATCH --account=pi_strow
#SBATCH -N1
#SBATCH --cpus-per-task=1
# Files are under 20G, see if 20G is enough for runs
#SBATCH --mem=20000
# runtime on strowinteract is about 17 minutes
#SBATCH --time=00:20:00

#SBATCH -o /home/sbuczko1/LOGS/sbatch/compress_era5-%A_%a.out
#SBATCH -e /home/sbuczko1/LOGS/sbatch/compress_era5-%A_%a.err

echo "Executing batch era5 compression"
$HOME/git/era5_pipeline/util/compress_era5_parallel.sh -v -f $1
echo "Era5 compression finished"
