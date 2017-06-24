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

#VEP
#variant_effect_predictor.pl --cache -i /proj/b2014152/nobackup/vanja/test_10X_2/outs/dels.vcf.gz -o output_test3.vcf --format vcf --vcf --port 3337 --force_overwrite

#TenexPipe main
python ./TenexPipe_tmp.py --folder /home/vanja/MasterProject/fastq_data/Tenex_folder --wgs

# This one works fine!
#~/nextflow /home/vanja/MasterProject/longranger_test/MasterProject/TenexPipe.nf --wgs --dry_run -c /home/vanja/MasterProject/longranger_test/MasterProject/TenexPipe.config

