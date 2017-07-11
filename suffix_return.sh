#!/bin/sh

#script used for changing back suffix 
#$1 

#module unload python3
#pip install python 2.7.6

#module load bioinfo-tools
#module load longranger
#module load vep

ls -l $1 | while read line; do  echo $line | sed s/.sample/''/; done