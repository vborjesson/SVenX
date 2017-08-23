# SVenX


Pipeline that uses 10x genomics fastq-data to find Structural variants, SVs. 
---
SVenX is a program that takes in fastq-files (single samples or folder of several samples) generated from 10x-genomics, the sample-folders will be checked if they contain all necessary files and execute user selected programs such as; Longranger WGS, VEP, TIDDIT, CNVnator, SVDB and filtering steps.

![alt text](https://github.com/vborjesson/SVenX/blob/master/SVenX_pipe.png)

### Environmental setup 
---

In order to run this program you will need to set up an environment. 

For all programs, Nextflow needs to be installed (https://www.nextflow.io/docs/latest/getstarted.html)

If Longranger wgs:
  If you are using UPPMAX just load the module longranger.
  Softwares; longranger + refdata (see https://www.10xgenomics.com), 

if VEP:
  If you are using UPPMAX just load the module vep/87.
  If you are not working on UPPMAX; VEP + cache file (VEP ENSMBLE website).

If TIDDIT:
  Just follow the instructions in setup.py.

If CNVnator:   
  If you are using UPPMAX, only load the module CNVnator and setup a reference directory.
  If you are not working on UPPMAX, please install the CNVnator from https://github.com/abyzovlab/CNVnatorat.

If TIDDIT or CNVnator:
  If you are using UPPMAX just load the module CNVnator. 
  You will need to merge the output vcf-files using SVDB. Installation is partly done using setup.py, but also requires sciKit-learn v0.15.2 as well as numpy.  

### RUN
---
Clone this repository.
```
git clone https://github.com/vborjesson/SVenX.git
python setup.py
```
I strongly recommend you to use a bash-script to launch SVenX. An example how your script can look like; SVenX.sh.  

```
python SVenX_main.py -h

usage: SVenX_main.py [-h] [--sample TENX_SAMPLE] [--folder TENX_FOLDER]
                     [--config CONFIG] [--dryrun] [--wgs] [--vep] [--TIDDIT]
                     [--CNVnator] [--annotation] [--basic] [--output OUTPUT]
                     [--nextflow NF]

SVenX takes fastq-samples generated from 10x-genomics and execute Assambly,
Variant calling, plots, stats etc. of the users choice

optional arguments:
  -h, --help            show this help message and exit
  --sample TENX_SAMPLE  Path to the 10x-genomics fastq folder
  --folder TENX_FOLDER  If you want to run several 10x-genomic samples at one
                        time, collect all in one folder and enter the path to
                        that folder
  --config CONFIG       Path to configuration file
  --dryrun              Add if you want to perform a dry run (good if testing
                        pipeline)
  --wgs                 Add if you want to run longranger wgs
  --vep                 Add if you want to run vep
  --TIDDIT              Add if you want to run variant calling - TIDDIT
  --CNVnator            Add if you want to run variant calling - CNVnator
  --annotation          Add if you want to run annotations
  --basic               Add if you want to run longranger basic
  --output OUTPUT       workingDir, is set to SVenX_outs as a default
  --nextflow NF         path to program nextflow, is set to ~/nextflow as
                        default


```
An example: 

``` 
python ./SVenX_main.py --sample /home/name/project/10x_fastq_data/Sample_P5357_1001 --wgs --vep --TIDDIT --CNVnator
```

2017-08-18
Test with tiny-data X 3 with soft links. running: 
python ./SVenX_main.py --folder /tiny/data/path/ --wgs --vep --TIDDIT --CNVnator
48 h 1 core 
- did not work! Out of memory. 

2017-08-21
Test with tiny-data X 2 with soft links. running: 
python ./SVenX_main.py --folder /tiny/data/path/ --wgs --vep --TIDDIT --CNVnator
120 h 2 core 
- did not work! Out of memory again.

2017-08-22
Test with tiny-data X 2 with soft links. running: 
python ./SVenX_main.py --folder /tiny/data/path/ --wgs --vep --TIDDIT --CNVnator
120 h 1 core and maxforks in process longranger wgs = 1
- still running. 

Added sorting to end of main-script 

