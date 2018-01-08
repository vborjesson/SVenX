# SVenX


Pipeline for SV detection using 10X genomics data 
---
SVenX is a highly parallelized pipeline taking fastq-files (single samples or folder of several samples) generated from 10x-genomics as input and execute variant calling, annotations, filtering and genotyping resulting in a vcf-file. 

![alt text](https://github.com/vborjesson/SVenX/blob/master/SVenX_pipe.png)

### Environmental setup 
---
Nextflow needs to be installed (https://www.nextflow.io/docs/latest/getstarted.html)

If you are working on a high performance cluster like UPPMAX:
```
Module load bioinfo-tools longranger vep/87 CNVnator samtools  
```
Download 
- refdata for longranger (see https://www.10xgenomics.com)
- CNVnator reference directory (https://github.com/abyzovlab/CNVnator)  
- SVDB requires sciKit-learn v0.15.2 and numpy. 

If you´re not working on a cluster:
Install VEP + cache file (VEP ENSMBLE website), CNVnator (https://github.com/abyzovlab/CNVnator
).

### Installation SVenX 
---
Clone this repository.
```
git clone https://github.com/vborjesson/SVenX.git
python setup.py
```

### RUN
---
Options
```
python SVenX_main.py -h

usage: SVenX_main.py [-h] [--sample TENX_SAMPLE] [--folder TENX_FOLDER]
                     [--config CONFIG] [--dryrun] [--vep] [--TIDDIT]
                     [--CNVnator] [--basic] [--output OUTPUT] [--nextflow NF]

SVenX takes fastq-samples generated from 10x-genomics and execute Assambly,
Variant calling, plots, stats etc. of the users choice

optional arguments:
  -h, --help            show this help message and exit
  --sample TENX_SAMPLE  Path to the 10x-genomics fastq folder
  --folder TENX_FOLDER  If you want to run several 10x-genomic samples at one
                        time, collect all in one folder and enter the path to
                        that folder
  --config CONFIG       Path to configuration file
  --dryrun              Add if you want to perform a dry run on longranger wgs (skip longranger wgs by adding path to already analyzed files by longranger wgs)
  --vep                 Add if you want to run vep
  --TIDDIT              Add if you want to run variant calling - TIDDIT
  --CNVnator            Add if you want to run variant calling - CNVnator
  --output OUTPUT       workingDir, is set to SVenX_outs as default
  --nextflow NF         path to program nextflow, is set to ~/nextflow as
                        default


```
An example: 

``` 
python ./SVenX_main.py --sample /home/name/project/10x_fastq_data/Sample_P3333_1001 --vep --TIDDIT --CNVnator
```
Or if you want to run several samples at the same time:
```
python ./SVenX_main.py --folder /home/name/project/10x_fastq_data --vep --TIDDIT --CNVnator
```

For WGS data, this pipeline takes approximately 5 days to run.   





