# SVenX


This is a pipeline in progress. It will include longranger wgs and basic, CNVnator, several ANNOTATION steps and more. 
---
SVenX is a program that takes in fastq-files (single samples or folder of several samples) generated from 10x-genomics, and execute Longranger WGS, Longranger BASIC, VEP, FindSV.. and more. 

In order to run this program you will need to set up an environment. 

For all programs, Nextflow needs to be installed (https://www.nextflow.io/docs/latest/getstarted.html)

If Longranger wgs:  
  Softwares; longranger + refdata (see https://www.10xgenomics.com), 

if VEP:
  VEP + cache file (VEP ENSMBLE website)

If TIDDIT:
  just follow the instructions in setup.py

If CNVnator:   
  If you are using UPPMAX, only load the module in your launching bash script. See SVenX.sh. And setup a reference directory.
  If you are not working on UPPMAX, please install the CNVnator from https://github.com/abyzovlab/CNVnatorat.

If TIDDIT or CNVnator:
  You will need to merge the output vcf-files using SVDB. Installation is partly done using setup.py, but also requires sciKit-learn v0.15.2 as well as numpy.  

Choose programs below that you would like to include in the SVenX-pipe

Longranger wgs 
VEP
TIDDIT
CNVnator
annotations
 
special: SV and annotation combine!

RUN
---
Clone this repository.
```
python setup.py
```
 
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

./SVenX.sh (or use sbatch)

```
-- suggestions that we might want to add: 
- Choose what you want to do; wgs and annotation (VEP, Frequence, 1kg, Swefreq, Exac, Gnomad, Score-model, CADD, Genemode), or wgs and SNVnator, TIDDIT (to find CNVs and rearrangements), SVDB, ..or just wgs and vep.  
-Add plots of SVs?
-Other cool stuff?   
```
2017-07-31

SVenX_07 test run with SVDB merge. 
  python ./SVenX_main.py --sample /home/vanja/MasterProject/fastq_data/Sample_P5357_1001 --wgs --vep --TIDDIT --CNVnator --dryrun
  -Works fine! generates a merge_callers.vcf in SVenX_outs

SVenX_08 test run with SVDB merge + vep_svdb (just vep) script
  -works fine  

For later: 

      - Create nf_script SVDB_query (vep-input) add to vep_svdb_template.

      - Pass-script in bash!  

      - As last script in nf-pipe: Create folders of samples

