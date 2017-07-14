# SVenX


This is a pipeline in progress. It will include longranger wgs and basic, CNVnator, several ANNOTATION steps and more. 
---
SVenX is a program that takes in fastq-files (single samples or folder of several samples) generated from 10x-genomics, and execute Longranger WGS, Longranger BASIC, VEP, FindSV.. and more. 

In order to run this program you will need to set up an environment. 
Nextflow needs to be downloaded. 

For all programs, Nextflow needs to be installed (https://www.nextflow.io/docs/latest/getstarted.html)

If Longranger wgs:  
  Softwares; longranger + refdata (see https://www.10xgenomics.com), 

if VEP:
  VEP + cache file (VEP ENSMBLE website)

If TIDDIT:
  just follow the instructions in setup.py

If CNV:   
  If you are using UPPMAX, only load the module in your launching bash script. See SVenX.sh. And setup a reference directory.
  If you are not working on UPPMAX, please install the CNVnator from https://github.com/abyzovlab/CNVnatorat.

Choose programs below that you would like to include in the SVenX-pipe

Longranger wgs 
VEP
TIDDIT
CNVnator
annotations
 
special: SV and annotation combine!

Clone this repository. 
Use SVenX.sh and add the desired parameters;

```
usage: SVenX_main.py [-h] [--sample TENX_SAMPLE] [--folder TENX_FOLDER]
                     [--config CONFIG] [--dryrun] [--wgs] [--vep] [--TIDDIT]
                     [--CNVnator] [--annotation] [--basic] [--output OUTPUT]
                     [--nextflow NF] [--wgs_script WGS_SCRIPT_NF]
                     [--vep_script VEP_SCRIPT_NF] [--TIDDIT_script TIDDIT.nf]
                     [--CNVnator_script CNVNATOR_SCRIPT_NF]
                     [--init_wgs_vep INIT_WGS_VEP]

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
  --output OUTPUT       workingDir
  --nextflow NF         path to program nextflow
  --wgs_script WGS_SCRIPT_NF
                        Path to longranger wgs nextflow script
  --vep_script VEP_SCRIPT_NF
                        Path to VEP nextflow script
  --TIDDIT_script TIDDIT.nf
                        Path to TIDDIT nextflow script
  --CNVnator_script CNVNATOR_SCRIPT_NF
                        Path to CNVnator nextflow script
  --init_wgs_vep INIT_WGS_VEP
                        Path to wgs_vep initiate script; init_wgs_vep.sh

..to be continued 

```

Run
---
```
./SVenX.sh

```
-- suggestions that we might want to add: 
- Choose what you want to do; wgs and annotation (VEP, Frequence, 1kg, Swefreq, Exac, Gnomad, Score-model, CADD, Genemode), or wgs and SNVnator, TIDDIT (to find CNVs and rearrangements), SVDB, ..or just wgs and vep.  
-Add plots of SVs?
-Other cool stuff?   
```
2017-07-14
Today I made a setup.py script. This script takes raw_input and set it as a template in a template config file that allready exist and make a new one called SVenX.conf. 
One problem is all the programs that needs several step installations and changes in root-system. Me and Jesper decided not to add the installation steps in this script. If the user wants to run that specific program he or she has to install it himself/herself. If using Uppmax this will not be as big of a problem.

Note til next time:
When testing the setup script, instead of returing /home/vanja/Master... it returns /??/???/vanja/Mast...

when trying to run the pipe with --wgs and --dryrun;

WARN: File `/home/vanja/MasterProject/fastq_data/TenX_folder/sample_1` is out of the scope of process working dir: /pica/h1/vanja/MasterProject/TEST_SVENX/SVenX/work/f0/0d1383d10cf8a7ae41cc3417bd6622 -- Error is ignored

Tested with --folder which works fine! something wrong with --sample?

next time; continue with setup.py. 

---

- 