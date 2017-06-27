#!/bin/bash -l

#SBATCH -A b2014152
#SBATCH -p core
#SBATCH -n 1
#SBATCH -t 24:00:00
#SBATCH -J TenexPipe_01

module load bioinfo-tools
module load longranger
module load vep

#module load python3

#longranger wgs
#longranger wgs --fastqs=/proj/b2016296/INBOX/P5357/Sample_P5357_1001 --id=sample2 --reference=~/MasterProject/fastq_data/refdata-hg19-2.1.0/

#TenexPipe main
python ./SVenX_main.py --folder /home/vanja/MasterProject/fastq_data/Tenex_folder --wgs


