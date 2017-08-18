
import os
import subprocess
import sys

answer = False

print '\n###################################################################################'
print '\n                       SVenX setup'
print '\n###################################################################################'
print ('\nFollow the instructions in this setup script and answer the questions when needed.')

# GENERAL

# Nextflow
print ('Parts of SVenX is written in Nextflow, in order to run it nextflow needs to be installed.')
print 'Is nextflow installed? yes/no'
while answer is False:
    selection=raw_input()
    if selection == 'NO' or selection == 'no':
        print('Please install nextflow and then run setup.py once again')
        sys.exit()  
    if selection == 'YES' or selection == 'yes':
        answer = True  
    else:
        print'Invalid syntax, please enter yes or no'    

# Uppmax or not, important when installing modules or programs.
print 'Do you plan to run SVenX on UPPMAX? yes/no'
answer = False
while answer is False:
    selection=raw_input()
    if selection == 'NO' or selection == 'no':
        uppmax = False  
        answer = True
    if selection == 'YES' or selection == 'yes':
        uppmax = True
        answer = True  
    else:
        print 'Invalid syntax, please enter yes or no'       

if not uppmax:
    print 'Longranger needs to be installed before running SVenX. Information about how to install it can be found at https://support.10xgenomics.com.'
    print 'Is longranger installed? yes/no'
    answer = False
    while answer is False:
        selection=raw_input()
        if selection == 'NO' or selection == 'no':
            print('Please install Longranger and then run setup.py once again')
            sys.exit()  
        if selection == 'YES' or selection == 'yes':
            answer = True  
        else:
            print 'Invalid syntax, please enter yes or no'

#SVenXDirectory = os 
SVenXDirectory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SVenXDirectory,"template/SVenX_template.config"), 'r') as myfile:
    template=myfile.read()

print 'General information needed in order to run Longranger.' 


print "Enter standard output directory, the path is set to SVenX_outs if left empty"
selection=raw_input()
if selection == "":
    selection = os.path.join(SVenXDirectory,"SVenX_outs")
template=template.replace("{working_dir}", "\'{}\'".format(selection) )

print "Set the path to the reference genome hg 19"
selection=raw_input()
template=template.replace("{ref_genome}", "\'{}\'".format(selection) )


# VEP 
print "Do you want to run VEP? yes/no"
selection = raw_input()
if selection == "yes" or selection == "YES": 
    answer = False
    if uppmax:
        print 'The module will be loaded on UPPMAX'
        answer = True
    if not uppmax:
        print 'In order to run VEP it has to be installed. Information about how to install it can be found at VEP ENSMBLE website.'
        print 'Is VEP installed? yes/no'        
        while answer is False:
            selection=raw_input()
            if selection == 'NO' or selection == 'no':
                print('\nPlease install VEP and then run setup.py once again')
                sys.exit()  
            if selection == 'YES' or selection == 'yes':
                answer = True  
            else:
                print 'Invalid syntax, please enter yes or no'


# TIDDIT
print "Do you want to run TIDDIT? yes/no"
selection = raw_input()
if selection == "yes" or selection == "YES": 
    print "TIDDIT needs to be installed in order to run it. If you have already installed TIDDIT, please answer no."
    print "Do you want to install TIDDIT? yes/no"
    selection = raw_input()
    if selection == 'yes' or selection == 'YES':
        print "installing and setting up TIDDIT"
        subprocess.call('chmod +x installation_scripts/install_TIDDIT.sh', shell=True)
        command=["{} {}".format(os.path.join(SVenXDirectory,"installation_scripts/install_TIDDIT.sh"),SVenXDirectory)]
        tmp=subprocess.check_output(command,shell = True)
        template=template.replace("{TIDDIT_path}", "\'{}\'".format(os.path.join(SVenXDirectory,"TIDDIT/bin/TIDDIT")) )

    if selection == 'no' or selection == 'NO':
        print 'Add path to TIDDIT. The path is set to current working directory TIDDIT/bin/TIDDIT/ if left blank'
        selection = raw_input()
        if selection == "":
            selection = os.path.join(SVenXDirectory,"TIDDIT/bin/TIDDIT")
        template=template.replace("{TIDDIT_path}", "\'{}\'".format(selection))

# SV - CNVnator
print "Do you want to run CNVnator? yes/no"
selection = raw_input()
if selection == "yes" or selection == "YES": 
    answer = False
    if uppmax:
        print 'The module will be loaded on UPPMAX'
        answer = True
    if not uppmax:
        print 'In order to run CNVnator it has to be installed. Information about how to install it can be found at https://github.com/abyzovlab/CNVnatorat .'
        print 'Is CNVnator installed? yes/no'        
        while answer is False:
            selection=raw_input()
            if selection == 'NO' or selection == 'no':
                print('Please install CNVnator and then run setup.py once again')
                sys.exit()  
            if selection == 'YES' or selection == 'yes':
                answer = True  
            else:
                print 'Invalid syntax, please enter yes or no'

    if answer:
        print "Enter path to CNVnator, the path is set to cnvnator if left blank"
        selection=raw_input()
        if selection == "":
            selection = "cnvnator"
        template=template.replace("{CNVnator_path}", "\'{}\'".format(selection) )

        print "Enter the cnvnator2VCF.pl script path, the path is set to cnvnator2VCF.pl if left blank"
        selection=raw_input()
        if selection == "":
            selection = "cnvnator2VCF.pl"
        template=template.replace("{CNVnator2vcf_path}", "\'{}\'".format(selection) )


        print "if the ROOTSYS variable is not set, add the path to the thisroot.sh script inside the root bin folder, leave blank otherwise(open another terminal and print echo $ROOTSYS to check)"
        selection=raw_input()
        template=template.replace("{thisroot_path}", "\'{}\'".format(selection) )
        thisroot=selection

        print "add the path of the directory containing reference files"
        selection=raw_input()
        template=template.replace("{CNVnator_reference_dir_path}", "\'{}\'".format(selection) )

print "If you are going to run TIDDIT or CNVnator, the vcf-files generated needs to be merged. In order to do so, SVDB needs to be installed. If you have already installed SVDB please answer no"
print "Do you want to install SVDB? yes/no"
selection = raw_input()
if selection == 'yes' or selection == 'YES':
    print "SVDB requires sciKit-learn v0.15.2 as well as numpy, if these have not been installed yet, please answer no and do so before starting over again"
    print "Have sciKit-learn v0.15.2 and numpy correctly been installed?"
    selection = raw_input()
    if selection  == 'no' or selection == 'NO':
        print('\nPlease make sure sciKit-learn v0.15.2 and numpy is installed and then run setup.py once again')
        sys.exit()  
    print "installing and setting up SVDB"
    subprocess.call('chmod +x installation_scripts/install_SVDB.sh', shell=True)
    command=["{} {}".format(os.path.join(SVenXDirectory,"installation_scripts/install_SVDB.sh"),SVenXDirectory)]
    tmp=subprocess.check_output(command,shell = True)
    template=template.replace("{SVDB_script_path}", "\'{}\'".format(os.path.join(SVenXDirectory,"SVDB/SVDB.py")) )


print  "In order to run SVDB query, please add the path to query database. See https://github.com/J35P312/SVDB for more information"
selection=raw_input()
template=template.replace("{SVDB_database}", "\'{}\'".format(selection) )

f= open('SVenX.conf', "w")
f.write(template)
f.close()

subprocess.call('chmod +x ./SVenX.sh', shell=True)