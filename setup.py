
import os
import subprocess
import sys

x = False

print 'SVenX setup'
print 'Follow the instructions in this setup and answer the questions when needed'

# GENERAL

# Nextflow
print ('/nParts of SVenX is written in Nextflow, in order to run it, nextflow needs to be installed')
print 'Is nextflow installed? yes/no'
while answer is False:
    selection=raw_input()
    if selection == 'NO' or selection == 'no':
        print('\nPlease install nextflow and then run setup.py once again')
        sys.exit()  
    if selection == 'YES' or selection == 'yes':
        answer = True  
    else:
        print 'Invalid syntax, please enter yes or no'    

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
            print('\nPlease install Longranger and then run setup.py once again')
            sys.exit()  
        if selection == 'YES' or selection == 'yes':
            answer = True  
        else:
            print 'Invalid syntax, please enter yes or no'

SVenXDirectory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SVenXDirectory,"SVenX_nf.config"), 'r') as myfile:
    template=myfile.read()

print 'General information needed in order to run Longranger'    

print "/nEnter standard output directory, the path is set to SVenX_outs if left empty"
selection=raw_input()
if selection == "":
    selection == "SVenX_outs"
template=template.replace("{working_dir}", "\'{}\'".format(selection) )

print "Set the path to the reference genome hg 19"
selection=raw_input()
template=template.replace("{ref_genome}", "\'{}\'".format(selection) )


print 'TIDDIT'
# SV - TIDDIT

print "TIDDIT needs to be installed in order to run it. If you have already installed TIDDIT, please answer no."
print "Do you want to install TIDDIT? yes/no"
selection = raw_input()
if selection == 'yes' or selection == 'YES':
    print "installing and setting up TIDDIT"
    subprocess.call('chmod +x install_TIDDIT.sh', shell=True)
    command=["{} {}".format(os.path.join(SVenXDirectory,"install_TIDDIT.sh"),SVenXDirectory)]
    tmp=subprocess.check_output(command,shell = True)
    template=template.replace("{TIDDIT_path}", "\'{}\'".format(os.path.join(SVenXDirectory,"TIDDIT/bin/TIDDIT")) )

# SV - CNVnator
print "Do you want to run CNVnator? yes/no"
selection = raw_input()
if selection == "yes" or selection == "YES": 
    answer == Flase
    if uppmax:
        answer == True
    if not uppmax:
        print 'In order to run CNVnator it has to be installed. Information about how to install it can be found at https://github.com/abyzovlab/CNVnatorat .'
        print 'Is CNVnator installed? yes/no'        
        while answer is False:
            selection=raw_input()
            if selection == 'NO' or selection == 'no':
                print('\nPlease install CNVnator and then run setup.py once again')
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


print "enter the filename of the new config file(or leave blank to set the config file to SVenX.conf)"
selection=raw_input()
if selection == "":
    selection = "SVenX.conf"
f= open(selection, "w")
f.write(template)
f.close()