#!/bin/bash -l

#SBATCH -A b2014152
#SBATCH -p core
#SBATCH -n 16
#SBATCH -t 48:00:00
#SBATCH -J SVenX_tinyData
#SBATCH --mail-type=ALL
#SBATCH --mail-user=vanja.borjesson@gmail.com

module load bioinfo-tools
module load longranger
module load vep/87
module load CNVnator

#SVenX main
pdcp * $TMPDIR 
cd $TMPDIR
python ./SVenX_main.py --folder /home/vanja/MasterProject/fastq_data/Sample_P5357_1001 --wgs --vep --TIDDIT --CNVnator
cp $TMPDIR/SVenX_out $SLURM_SUBMIT_DIR 
