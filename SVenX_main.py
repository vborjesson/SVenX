#!/usr/bin/python

'''
Main script for TenexPipe
'''

import sys
import os 
import csv
import argparse
import subprocess

################# ARGPARSER ######################

usage = '''SVenX takes fastq-samples generated from 10x-genomics and execute Assambly, Variant calling, plots, stats etc. of the users choice''' 

parser = argparse.ArgumentParser(description=usage)

parser.add_argument(
	'--sample', 
	metavar='tenX_sample',
	dest='tenX_sample',
	help = 'Path to the 10x-genomics fastq folder',
	required= False
	)

parser.add_argument(
	'--folder', 
	metavar='tenX_folder',
	dest='tenX_folder',
	help = 'If you want to run several 10x-genomic samples at one time, collect all in one folder and enter the path to that folder', 
	required= False
	)

parser.add_argument(
	'--dryrun',
	dest = 'dryrun',
	help = 'If no samples added, please use this dryrun',
	action = 'store_true'
	)

parser.add_argument(
	'--wgs',
	#metavar = 'Longranger_wgs',
	dest='l_wgs',
	help= 'Add if you want to run longranger wgs',
	action='store_true',
	#type=argparse.FileType('r'),
	#required= False
	)

parser.add_argument(
	'--basic',
	#metavar = 'Longranger_wgs',
	dest='l_basic',
	help= 'Add if you want to run longranger basic',
	action='store_true',
	#type=argparse.FileType('r'),
	#required= False
	)

parser.add_argument(
	'--config',
	metavar = 'config-file',
	dest='config',
	default= './TenexPipe.config',
	help='Add configuration file',
	#type=argparse.FileType('w'),
	required= False
	)


parser.add_argument(
	'--output',
	metavar = 'Output',
	dest='output',
	default='./Longranger_out',
	help='workingDir',
	#type=argparse.FileType('w'),
	required= False
	)

parser.add_argument(
	'--nextflow',
	metavar = 'nextflow',
	dest='nf',
	default= '~/nextflow', 
	help='path to program nextflow',
	#type=argparse.FileType('w'),
	required= False
	)

parser.add_argument(
	'--LongrangerNF',
	metavar = 'longrnager_wgs.nf',
	dest='LongWGS',
	default= './longranger_wgs.nf',
	help='Path to longranger wgs nextflow script',
	#type=argparse.FileType('w'),
	required= False
	)

parser.add_argument(
	'--launch_longranger',
	metavar = 'launch_longranger',
	dest='longranger_init',
	default= './launch_longranger.sh',
	help='Path to Longranger initiate script; launch_longranger.sh',
	#type=argparse.FileType('w'),
	required= False
	)


args = parser.parse_args()
tenX_folder = args.tenX_folder
tenX_sample = args.tenX_sample
dry_run = args.dryrun
wgs = args.l_wgs
basic = args.l_basic
folder_list = []
folder_path = ''
TenX_path = ''
ID_path = {}

############################ CHECK SAMPLE CONTENTS -FUNCTIONS ################################## 

# Read in the 10x-genomics fastq-files and check weather they are complete or not. 
# If not completed or if only one sample is added, the program will break and return an error message. If all folders and files are in order, their path will be saved in a list. 

def check_folders (folder_file):
	print('Checking if all samples in folder containes all three fastq-files; I1, R1 and R2.\n')

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
				if ('I1_001.fastq.gz' in file):
					I1 = True
				if ('R1_001.fastq.gz' in file):
					R1 = True
				if ('R2_001.fastq.gz' in file):
					R2 = True

			if not (I1 and R1 and R2):
				print '\nError: This sample', root, 'is not complete, please check it and try again.' 	
				sys.exit()

			if (I1 and R1 and R2):
				folder_list.append(root)
				print root.split('/')[-1], 'is checked and complete.'

		else:
			print '\nError, wrong number of files in folder ', root, '. Three fastq-files are recuired, please check the folder and try again.'
			sys.exit()

	if (len(folder_list)) == 0:
		print '\nError, something went wrong reading the folders. Make sure the folders path you added consists of several sample-folders. If you want to add just one sample, please use the argument -s [sample instead]'
		sys.exit()	
	
	else:
		return(folder_list)	


# Read in the 10x-genomics fastq-sample-folder and check weather this is complete or not. 
# If not completed, the program will break and return an error message. If all files are correct, the path will be saved in folder_list. 

def check_sample (sample_file):
	fastq_list = os.listdir(sample_file)
	print 'the sample ', sample_file.split('/')[-1], 'will be checked if it is complete'
	if len(fastq_list) == 3: 
		I1 = False
		R1 = False
		R2 = False 
		for file in fastq_list:
		#print('three files exist in this file')

			if ('I1_001.fastq.gz' in file):
				I1 = True
			if ('R1_001.fastq.gz' in file):
				R1 = True
			if ('R2_001.fastq.gz' in file):
				R2 = True

			#print('all three files I1 R1 and R2 was found')
			#print('Sample', sample_file, 'is checked and complete')
		if not (I1 and R1 and R2):
			print('\nError: This sample is not complete, please check it and try again.') 	
			sys.exit()
	else: 
		print('\nError, this sample have the wrong number of fastq-files, please check that all three I1. R1 and R2 exist and try again.')
		sys.exit()

	return(sample_file)


#################################### LONGRANGER - VEP #############################################################

def longranger_vep (sh_init_script, nextflow_path, nextflow_script, sample, config, output, sample_type): # sample_type = folder or sample
	# Create script longranger - vep 
	subprocess.call(['cat', args.longranger >> test1.txt')

#################################### INITIATE LONGRANGER WGS AND BASIC -FUNCTIONS ##################################

def longranger (sh_init_script, nextflow_path, nextflow_script, sample, config, output, sample_type): # sample_type = folder or sample

	if dry_run:
		print('\nDry run is initiated.. \n')
		process = [sh_init_script, nextflow_path, nextflow_script, '--dry_run', '--wgs', config, output, sample_type]
		os.system(" ".join(process))	

	elif wgs:	
		print('\nLongranger wgs is initiated.')
		process = [sh_init_script, nextflow_path, nextflow_script, sample, '--wgs', config, output, sample_type]
		os.system(" ".join(process))	

	elif basic:	
		print('\nlongranger basic is initiated\n')
		process = [sh_init_script, nextflow_path, nextflow_script, sample, '--basic', config, output, sample_type]
		os.system(" ".join(process))

	else:
		print('\nerror; in order for longranger to work you have to specify wgs, basic or dry_run')	


################################### TERMINAL MESSAGE #############################################################

print('\n--------------------------------------------------------------------------------------------------------\n')
print('TenexPipe')
print('Version: 0.0.1') 
print('Author: Vanja Borjesson') 
print('Usage: https://github.com/vborjesson/MasterProject.git \n')
print('---------------------------------------------------------------------------------------------------------\n') 

#################################### MAIN SCRIPT -  ###############################################


# If a folder of folders with 10x data - this will initiate a function that checks that all folders and files are added correctly. 
if tenX_folder:
	tenX_path = check_folders(tenX_folder) 			

	if tenX_path:
		print('\nAll samples are checked and complete.')
		#print('tenX_path from function checked', tenX_path)

		# Longranger wgs is initiated through bash and nextflow with checked folders as input. 
		process_longranger = longranger(args.longranger_init, args.nf, args.LongWGS, tenX_folder, args.config, args.output, '--folder') 


# if only one sample; this one is checked separately i fall files exist. Send to longranger if recuired. 
if tenX_sample:
	tenX_path = check_sample(tenX_sample)
	if tenX_path:
		print('\nThe sample is checked and complete')		
		if wgs or basic:
			process_longranger = longranger(args.longranger_init, args.nf, args.LongWGS, tenX_path, args.config, args.output, '--sample') 


##################################### IF #########################################################################################



