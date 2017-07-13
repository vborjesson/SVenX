#!/bin/sh

#script used for automated launching of SVenX.nf.
#$1 Path to nextflow 
#$2 10X samples (or dry_run) 
#$3 configuration file 
#$4 the output directory(aka publishdir)
#$5 Sample type; folder or sample
#$6 if dryrun

#module unload python3
#pip install python 2.7.6

#module load bioinfo-tools
#module load longranger
#module load vep
#module load 

$1 SVenX.nf --fastq $2 --wgs -c $3 --workingDir $4 $5 $6