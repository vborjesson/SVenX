#!/bin/sh

#script used for automated launcing of TenexPipe.nf.
#$1 Path to nextflow 
#$2 Path to nextflow script; TenexPipe.nf
#$3 10X samples (or dry_run) 
#$4 longranger wgs or basic?
#$5 configuration file 
#$6 the output directory(aka publishdir)
#$7 Sample type; folder or sample

#module unload python3
#pip install python 2.7.6

#module load bioinfo-tools
#module load longranger
#module load vep

$1 $2 --fastq $3 $4 -c $5 --workingDir $6 $7



