#!/usr/bin/python
# coding=utf-8

'''
Main script for TenexPipe
'''

import sys
import os 
import argparse
import subprocess

################# ARGPARSER ######################

usage = '''SVenX takes fastq-samples generated from 10x-genomics and execute Assambly, Variant calling, plots, stats etc. of the users choice''' 

parser = argparse.ArgumentParser(description=usage)

parser.add_argument('--sample', dest='tenX_sample', help = 'Path to the 10x-genomics fastq folder', required= False)
parser.add_argument('--folder', dest='tenX_folder', help = 'If you want to run several 10x-genomic samples at one time, collect all in one folder and enter the path to that folder', required= False)
parser.add_argument('--config', dest='config', default= 'SVenX.conf', help='Path to configuration file', required= False)
parser.add_argument('--dryrun', dest = 'dryrun', help = 'Add if you want to perform a dry run (good if testing pipeline)', action = 'store_true')
parser.add_argument('--wgs', dest='l_wgs', help= 'Add if you want to run longranger wgs', action='store_true', required= False)
parser.add_argument('--vep', dest='vep', help= 'Add if you want to run vep', action = 'store_true') 
parser.add_argument('--TIDDIT', dest= 'TIDDIT', help= 'Add if you want to run variant calling - TIDDIT', action= 'store_true')
parser.add_argument('--CNVnator', dest= 'CNVnator', help= 'Add if you want to run variant calling - CNVnator', action= 'store_true')
parser.add_argument('--annotation', dest = 'annotation', help= 'Add if you want to run annotations', action= 'store_true')
parser.add_argument('--basic', dest='l_basic', help= 'Add if you want to run longranger basic', action='store_true', required= False)

parser.add_argument('--output', dest='output', default='SVenX_outs', help='workingDir, is set to SVenX_outs as default', required= False)
parser.add_argument('--nextflow', dest='nf', default= '~/nextflow', help='path to program nextflow, is set to ~/nextflow as default', required= False)

'''
parser.add_argument('--wgs_script', dest='wgs_script_nf', default= 'nextflow_scripts/longranger_wgs.nf', help='Path to longranger wgs nextflow script, is set to script', required= False)
parser.add_argument('--vep_script', dest='vep_script_nf', default= 'nextflow_scripts/VEP.nf', help='Path to VEP nextflow script', required= False)
parser.add_argument('--TIDDIT_script', dest='TIDDIT_script_nf', default= 'nextflow_scripts/TIDDIT.nf', help='Path to TIDDIT nextflow script', required= False)
parser.add_argument('--CNVnator_script', dest='CNVnator_script_nf', default= 'nextflow_scripts/CNVnator.nf', help='Path to CNVnator nextflow script', required= False)
parser.add_argument('--annotation_script', dest='annotation_script_nf', default= 'nextflow_scripts/annotation.nf', help='Path to annotation nextflow script', required= False)
parser.add_argument('--launch_SVenX_nf', dest='launch_SVenX_nf', default= './launch_SVenX.sh', help='Path to SVenX nextflow launching script; launch_SVenX.sh, is set to ./launch_SVenX.sh', required= False)
'''

# Path to all nextflow scripts
wgs_script_nf= 'nextflow_scripts/longranger_wgs.nf'
vep_script_nf= 'nextflow_scripts/VEP.nf'
TIDDIT_script_nf='nextflow_scripts/TIDDIT.nf'
CNVnator_script_nf='nextflow_scripts/CNVnator.nf'
annotation_script_nf = 'nextflow_scripts/annotation.nf'
launch_SVenX_nf='./launch_SVenX.sh'

args = parser.parse_args()

tenX_folder = args.tenX_folder
tenX_sample = args.tenX_sample

# Programs 
dry_run = args.dryrun
wgs = args.l_wgs
vep = args.vep 
TIDDIT = args.TIDDIT
CNVnator = args.CNVnator
annotation = args.annotation
basic = args.l_basic

# defining lists, strings etc. 
folder_list = []
tenX_type = ''
program_list = []

# create list of programs that will be executed
if wgs:
	program_list.append('wgs')
if vep:
	program_list.append('vep')	
if TIDDIT:
	program_list.append('TIDDIT')
if CNVnator:
	program_list.append('CNVnator')	
if annotation:
	program_list.append('annotation')		

############################ CHECK SAMPLE CONTENTS -FUNCTIONS ################################## 

# Read in the 10x-genomics fastq-files and check weather they are complete or not. 
# If not completed or if only one sample is added, the program will break and return an error message. If all folders and files are in order, their path will be saved in a list. 

def check_folders (folder_file):
	print('Checking if all samples in folder contains all three fastq-files; I1, R1 and R2.\n')

	for root, dirs, files in os.walk(folder_file, topdown=False, followlinks=True):
		#print(root, dirs, files)
		if root == folder_file: # folder_path is also included in files, but we do not want this one in our list.
			continue
		
		if len(files) == 3:
			I1 = False
			R1 = False
			R2 = False 
			
			#print('Three files was found in this root', root)
			for file in files:
				if ('I1' in file):
					I1 = True
				if ('R1' in file):
					R1 = True
				if ('R2' in file):
					R2 = True

			if not (I1 and R1 and R2):
				print root, '\nError: This sample is not complete, please check it and try again.' 	
				sys.exit()

			if (I1 and R1 and R2):
				folder_list.append(root) # For sorting in end of script	
				print root.split('/')[-1], 'is checked and complete.'

		else:
			print root, '\nError, wrong number of files in folder. Three fastq-files are required, please check the folder and try again.'
			sys.exit()

	if (len(folder_list)) == 0:
		print '\nError, something went wrong reading the folders. Make sure the folders path you added consists of several sample-folders. If you want to add just one sample, please use the argument -s [sample instead]'
		sys.exit()	
	
	else:
		return(folder_file)	


# Read in the 10x-genomics fastq-sample-folder and check weather this is complete or not. 
# If not complete, the program will break and return an error message. If all files in sample are correct, the path will be returned. 

def check_sample (sample_file):
	fastq_list = os.listdir(sample_file)
	print 'the sample', sample_file.split('/')[-1], 'will be checked if it is complete'
	if len(fastq_list) == 3: 
		I1 = False
		R1 = False
		R2 = False 
		for file in fastq_list:
		#print('three files exist in this file')

			if ('I1' in file):
				I1 = True
			if ('R1' in file):
				R1 = True
			if ('R2' in file):
				R2 = True	

		if not (I1 and R1 and R2):
			print('Error: This sample is not complete, please check it and try again.') 	
			sys.exit()
	else: 
		print('Error, this sample have the wrong number of fastq-files, please check that all three I1. R1 and R2 exist and try again.')
		sys.exit()

	folder_list.append(sample_file) # For sorting in end of script	
	return(sample_file)


#################################### FUNCTION CREATE SCRIPT #################################################################

def create_script (wgs_script, vep_script, TIDDIT_script, CNVnator_script, annotation_script, program_list):
	
	# If TIDDIT or CNVnator; create a user-specific SVDB nextflow-script using a template. This is due to nextflow-specific inputs, outputs from 
	# different processes needs to be crossed before used as new input in new process. If TIDDIT and/or CNVnator have been executed; we want to 
	# merge the cnv-files using SVDB merge before continuing.    
	if ('TIDDIT' in program_list) or ('CNVnator' in program_list):
		print 'creating SVDB_merge script'

		SVenXDirectory = os.path.dirname(os.path.abspath(__file__))
		with open(os.path.join(SVenXDirectory,"template/SVDB_merge_template.nf"), 'r') as myfile:
			template=myfile.read()

		if ('TIDDIT' in program_list) and ('CNVnator' in program_list):
			template= template.replace("©©©©©", "wgs_outs_SVDB.cross(TIDDIT_output).map{it ->  [it[0][0],it[0][1],it[0][2],it[0][3],it[0][4],it[1][1]]}") 	
			template= template.replace("@@@@@", "combined_first.cross(CNVnator_output).map{it ->  [it[0][0],it[0][1],it[0][2],it[0][3],it[0][4],it[0][5],it[1][1]]}")
			template= template.replace("¤¤¤¤¤", "bam, dels_vcf, large_svs_vcf, phased_variants_vcf, TIDDIT_vcf, CNVnator_vcf")
			template= template.replace("£££££", "${large_svs_vcf} ${TIDDIT_vcf} ${CNVnator_vcf}")

		elif ('TIDDIT' in program_list):
			template= template.replace("©©©©©", "not_in_use")
			template= template.replace("@@@@@", "wgs_outs_SVDB.cross(TIDDIT_output).map{it ->  [it[0][0],it[0][1],it[0][2],it[0][3],it[0][4],it[1][1]]}")
			template= template.replace("¤¤¤¤¤", "bam, dels_vcf, large_svs_vcf, phased_variants_vcf, TIDDIT_vcf")
			template= template.replace("£££££", "${large_svs_vcf} ${TIDDIT_vcf}")

		elif ('CNVnator' in program_list):
			template= template.replace("©©©©©", "not_in_use")
			template= template.replace("@@@@@", "wgs_outs_SVDB.cross(CNVnator_output).map{it ->  [it[0][0],it[0][1],it[0][2],it[0][3],it[0][4],it[1][1]]}")
			template= template.replace("¤¤¤¤¤", "bam, dels_vcf, large_svs_vcf, phased_variants_vcf, CNVnator_vcf")
			template= template.replace("£££££", "${large_svs_vcf} ${CNVnator_vcf}")

		f= open('SVDB_merge.nf', "w")
		f.write(template)
		f.close()

		print 'SVDB merge script created'	
		
		print 'Creating VEP and SVDB query script specific for SVDB merge output files'

		SVenXDirectory = os.path.dirname(os.path.abspath(__file__))
		with open(os.path.join(SVenXDirectory,"template/vep_svdb_template.nf"), 'r') as myfile:
			my_files=myfile.read()

		my_files= my_files.replace("¤¤¤¤", "set ID, merged_callers from SVDB_merge_outout")
		my_files= my_files.replace("&&&&", "${merged_callers}")		

		f= open('VEP_SVDB.nf', "w")
		f.write(my_files)
		f.close()			

		print 'VEP_SVDB.nf script created'


	else: 	
		print 'creating vep and SVDB query script for longranger wgs large_svs.vcf'

		SVenXDirectory = os.path.dirname(os.path.abspath(__file__))
		with open(os.path.join(SVenXDirectory,"template/vep_svdb_template.nf"), 'r') as myfile:
			my_files=myfile.read()

		my_files= my_files.replace("¤¤¤¤", "set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from wgs_outs_vep")
		my_files= my_files.replace("&&&&", "${large_svs_vcf}")		

		f= open('VEP_SVDB.nf', "w")
		f.write(my_files)
		f.close()		

		print 'VEP_SVDB.nf script created'

	print 'Creating SVenX main nextflow script'
	with open('SVenX.nf', 'w') as outfile:
		
		if ('wgs' in program_list):
			subprocess.call('cat ' + str(wgs_script), shell=True, stdout=outfile)
			print 'Longranger wgs was added to the SVenX script'
		if ('vep' in program_list):
			subprocess.call('cat '+ str(vep_script), shell=True, stdout=outfile)
			print 'VEP was added to the SVenX script'	
		if ('TIDDIT' in program_list):
			subprocess.call('cat '+ str(TIDDIT_script), shell=True, stdout=outfile)
			print 'TIDDIT was added to the SVenX script'
		if ('CNVnator' in program_list):
			subprocess.call('cat '+ str(CNVnator_script), shell=True, stdout=outfile)
			print 'CNVnator was added to the SVenX script'
		if ('TIDDIT' in program_list) or ('CNVnator' in program_list):
			subprocess.call('cat SVDB_merge.nf', shell=True, stdout=outfile)
			print 'SVDB_merge was added to SVenX script'
			subprocess.call('cat VEP_SVDB.nf', shell=True, stdout=outfile)
			print 'vep and SVDB query was added to SVenX script'

		if ('annotation' in program_list):
			subprocess.call('cat '+ str(annotation_script), shell=True, stdout=outfile)
			print 'Annotation programs was added to the SVenX script'
			
		print 'Script completed\n'


#################################### FUNCTION LAUNCHING SVENX.NF #############################################################

# This function will launch the SVenX script with the user specific programs 
def launch_script (launch_SVenX_nf, nextflow_path, sample, config, output, sample_type):
	
	subprocess.call('chmod +x ' + str(launch_SVenX_nf), shell = True) 

	if dry_run:
		print 'Initiating dry run\n'
		process = [launch_SVenX_nf, nextflow_path, sample, config, output, sample_type, '--dry_run']
		os.system(" ".join(process))

	else: 
		print 'launching SVenX in nextflow\n'
		process = [launch_SVenX_nf, nextflow_path, sample, config, output, sample_type]
		os.system(" ".join(process))	


##################################### FUNCTION OUTPUT SORTING #############################################################

# This function sorts the folder with output-files generated by SvenX-nextflow. 
def sorting (sample_path, output_path):
	print 'Sorting files'
	for path in sample_path:
		sample_id = path.split('/')[-1]
		subprocess.call('mkdir ' + output_path + '/' + sample_id, shell=True)
		subprocess.call('mv ' + output_path + '/' + sample_id + '?* ' + output_path + '/' + sample_id, shell=True)


######################################## TERMINAL MESSAGE #############################################################

print('\n--------------------------------------------------------------------------------------------------------\n')
print('SVenX')
print('Version: 0.0.0') 
print('Author: Vanja Borjesson') 
print('Usage: https://github.com/vborjesson/SVenX.git \n')
print('---------------------------------------------------------------------------------------------------------\n') 

######################################### MAIN SCRIPT ############################################################

# If no sample added: message	
if not (tenX_folder or tenX_sample):
	print 'No 10X sample was added, please add a 10X sample or folder of samples as an argument and try again\n'
	sys.exit()

# If no programs was added as argument
if len(program_list) == 0:
	print 'No programs was selected. If you want to run any programs, please add program as argument when running SVenX. Please use SVenX_main.py -h for further information and options\n'
	sys.exit()		

if 'wgs' not in program_list:
	print 'In order to run the program you want, --wgs needs to be added as an argument to generate bam and vcf-files\n'	
	sys.exit()

# If a folder of folders with 10x data - this will initiate a function that checks that all folders and files are added correctly. 
if tenX_folder:
	folder_complete = check_folders(tenX_folder)
	tenX_type = '--folder' 			
	if folder_complete:
		print('\nAll samples are checked and complete.\n')

# I a sample of 10x data - this sample will be checked if it contain all fastq-files needed. 
if tenX_sample:
	folder_complete = check_sample(tenX_sample)
	tenX_type = '--sample' 
	if folder_complete:
		print('\nThe sample is checked and complete\n')

# Create a nextflow script with all selected programs
# Launch SVenX in nextflow
if program_list != '':
	make_script = create_script(wgs_script_nf, vep_script_nf, TIDDIT_script_nf, CNVnator_script_nf, annotation_script_nf, program_list) 			
	execute = launch_script(launch_SVenX_nf, args.nf, folder_complete, args.config, args.output, tenX_type)

# Sort the SVenX-folder containing output-files according to sample-name. 
sort = sorting(folder_list, args.output)

print 'SvenX have been successfully completed.' 
