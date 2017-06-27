# SVenX


This is a pipeline in progress. It will include longranger wgs and basic, FindSV, CNVnator, TIDDIT, SVDB, several ANNOTATION steps and more. 
---
SVenX is a program that takes in fastq-files (single samples or folder of several samples) generated from 10x-genomics, and execute Longranger WGS, Longranger BASIC, VEP, FindSV.. and more. 

In order to run this program you will need to set up an environment. 
Softwares; longranger + refdata (see https://www.10xgenomics.com), VEP + cache file (VEP ENSMBLE website) and nextflow

Clone this repository. 
Use SVenX.sh and add the desired parameters;
```
usage: TenexPipe.py [-h] [-s tenX_sample] [-f tenX_folder] [--dryrun] [--wgs]
                    [--basic] [--config config-file] [--output Output]

SVenX takes fastq-samples generated from 10x-genomics and execute
Assambly, Variant calling, plots, stats etc. of the users choice

optional arguments:
  -h, --help            show this help message and exit
  -s tenX_sample        Path to the 10x-genomics fastq folder
  -f tenX_folder        If you want to run several 10x-genomic samples at one
                        time, collect all in one folder and enter the path to
                        that folder
  --dryrun              If no samples added, please use this dryrun
  --wgs                 Add if you want to run longranger wgs
  --basic               Add if you want to run longranger basic
  --config config-file  Add config-file
  --output Output       workingDir

..to be continued 

```

Run
---
```
./SVenX.sh

```
-- suggestions that we might want to add: 
- Choose what you want to do; wgs and annotation (VEP, Frequence, 1kg, Swefreq, Exac, Gnomad, Score-model, CADD, Genemode), or wgs and SNVnator, TIDDIT (to find CNVs and rearrangments), SVDB, ..or just wgs and vep.  
-Add plots of SVs?
-Other cool stuff?   
```
---
As it looks today, this program runs from masterPipe.sh to core script TenexPipe.py, from there it goes through launch_core.sh to TenexPipe.nf. 
--Do we want the annotation step separetely from longranger?