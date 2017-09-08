#!/bin/bash -l

#SBATCH -A b2016296
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
module load samtools

#SVenX main
#cp -r * $TMPDIR 
#cd $TMPDIR
python ./SVenX_main.py --folder /proj/b2016296/private/vanja/test_data --wgs --vep --TIDDIT --CNVnator
#cp $TMPDIR/SVenX_outs $SLURM_SUBMIT_DIR 
