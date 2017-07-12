#!/bin/sh

#script used for automated launching of TenexPipe.nf.
#$1 Path to nextflow 
#$2 Path to nextflow script; wgs_vep.nf
#$3 10X samples (or dry_run) 
#$4 configuration file 
#$5 the output directory(aka publishdir)
#$6 Sample type; folder or sample
#$7 if dryrun

#module unload python3
#pip install python 2.7.6

#module load bioinfo-tools
#module load longranger
#module load vep
#module load 
$1 $2 --fastq $3 --wgs -c $4 --workingDir $5 $6 $7
