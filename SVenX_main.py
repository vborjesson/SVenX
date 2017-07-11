#!/usr/bin/python

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
	'--config',
	metavar = 'config-file',
	dest='config',
	default= './SVenX_nf.config',
	help='Path to configuration file',
	#type=argparse.FileType('w'),
	required= False
	)

parser.add_argument(
	'--dryrun',
	dest = 'dryrun',
	help = 'Add if you want to perform a dry run (good if testing pipeline)',
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
	'--vep',
	dest='vep',
	help= 'Add if you want to run vep',
	action = 'store_true'
	) 

parser.add_argument(
	'--variant_calling', 
	dest= 'variant_calling',
	help= 'Add if you want to run variant calling',
	action= 'store_true'
	)

parser.add_argument(
	'--annotation', 
	dest = 'annotation',
	help= 'Add if you want to run annotations')

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
	'--output',
	metavar = 'Output',
	dest='output',
	default='./SVenX_outs',
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
	'--wgs_script',
	metavar = 'longranger_wgs.nf',
	dest='wgs_script_nf',
	default= 'longranger_wgs.nf',
	help='Path to longranger wgs nextflow script',
	#type=argparse.FileType('w'),
	required= False
	)

parser.add_argument(
	'--vep_script',
	metavar = 'vep.nf',
	dest='vep_script_nf',
	default= 'VEP.nf',
	help='Path to VEP nextflow script',
	#type=argparse.FileType('w'),
	required= False
	)

parser.add_argument(
	'--init_wgs_vep',
	metavar = 'initiate_wgs_vep',
	dest='init_wgs_vep',
	default= './init_wgs_vep.sh',
	help='Path to wgs_vep initiate script; init_wgs_vep.sh',
	#type=argparse.FileType('w'),
	required= False
	)


args = parser.parse_args()

tenX_folder = args.tenX_folder
tenX_sample = args.tenX_sample

# Programs 
dry_run = args.dryrun
wgs = args.l_wgs
vep = args.vep 
variant_calling = args.variant_calling
annotation = args.annotation
basic = args.l_basic

# defining lists, strings etc. 
folder_list = []
tenX_type = ''

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
				folder_list.append(root)
				print root.split('/')[-1], 'is checked and complete.'

		else:
			print root, '\nError, wrong number of files in folder. Three fastq-files are required, please check the folder and try again.'
			sys.exit()

	if (len(folder_list)) == 0:
		print '\nError, something went wrong reading the folders. Make sure the folders path you added consists of several sample-folders. If you want to add just one sample, please use the argument -s [sample instead]'
		sys.exit()	
	
	else:
		print folder_file
		return(folder_file)	


# Read in the 10x-genomics fastq-sample-folder and check weather this is complete or not. 
# If not complete, the program will break and return an error message. If all files in sample are correct, the path will be returned. 

def check_sample (sample_file):
	fastq_list = os.listdir(sample_file)
	print 'the sample ', sample_file.split('/')[-1], 'will be checked if it is complete'
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
			print('\nError: This sample is not complete, please check it and try again.') 	
			sys.exit()
	else: 
		print('\nError, this sample have the wrong number of fastq-files, please check that all three I1. R1 and R2 exist and try again.')
		sys.exit()

	return(sample_file)


#################################### FUNCTION LONGRANGER WGS - VEP #############################################################

def wgs_vep (sh_init_script, nextflow_path, wgs_script, vep_script, sample, config, output, sample_type):

	print 'Creating wgs-vep script'

	# Create script
	with open('wgs_vep.nf', 'w') as outfile:
		subprocess.call('cat ' + str(wgs_script), shell=True, stdout=outfile)
		subprocess.call('cat '+ str(vep_script), shell=True, stdout=outfile)
		print 'Script completed'

	subprocess.call('chmod +x ' + sh_init_script, shell=True)
	
	# initiate longranger wgs and vep in nextflow
	if dry_run:
		print 'Initiating dryrun'
		process = [sh_init_script, nextflow_path, 'wgs_vep.nf', sample, config, output, sample_type, '--dry_run']
		os.system(" ".join(process))

		#subprocess.call(str(sh_init_script) + " " + str(nextflow_path) + ' wgs_vep.nf ' + str(sample) + " " + str(config) + " " + str(output) + " " + str(sample_type) + ' --dry_run', shell = True)

	else: 
		subprocess.call([sh_init_script, nextflow_path, 'wgs_vep.nf', sample, config, output, sample_type], shell = True)

		print 'Longranger wgs and vep have successfully been executed'	




'''
def wgs_vep (sh_init_script, nextflow_path, wgs_script, vep_script, sample, config, output, sample_type):
	process1 = ['cat', wgs_script, '>>', 'wgs_vep.nf', '|', 'cat', vep_script, '>>', 'wgs_vep.nf']
	os.system(" ".join(process1))
	process2 = [sh_init_script, nextflow_path, './wgs_vep.nf', sample, config, output, sample_type]
	os.system(" ".join(process2))
'''

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
print('SVenX')
print('Version: 0.0.0') 
print('Author: Vanja Borjesson') 
print('Usage: https://github.com/vborjesson/MasterProject.git \n')
print('---------------------------------------------------------------------------------------------------------\n') 

#################################### MAIN SCRIPT -  ###############################################


# If a folder of folders with 10x data - this will initiate a function that checks that all folders and files are added correctly. 
if tenX_folder:
	folder_complete = check_folders(tenX_folder)
	tenX_type = '--folder' 			
	if folder_complete:
		print('\nAll samples are checked and complete.')

# I a sample of 10x data - this sample will be checked if it coiontain all fastq-files needed. 
if tenX_sample:
	folder_complete = check_sample(tenX_sample)
	tenX_type = '--sample' 
	if folder_complete:
		print('\nThe sample is checked and complete')			

if wgs and vep:
	initiate_wgs_vep = wgs_vep(args.init_wgs_vep, args.nf, args.wgs_script_nf, args.vep_script_nf, folder_complete, args.config, args.output, tenX_type) 
	print 'wgs and vep executed'

