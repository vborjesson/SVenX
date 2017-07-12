
import os
import subprocess

# GENERAL
SVenXDirectory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SVenXDirectory,"SVenX_nf.config"), 'r') as myfile:
    template=myfile.read()

print "Enter standard output directory, the path is set to SVenX_outs if left empty"
selection=raw_input()
if selection == "":
    selection == "SVenX_outs"
template=template.replace("{working_dir}", "\'{}\'".format(selection) )

print "Set the path to the reference genome hg 19"
selection=raw_input()
template=template.replace("{ref_genome}", "\'{}\'".format(selection) )

# SV - TIDDIT
print "installing and setting up TIDDIT"
command=["{} {}".format(os.path.join(SVenXDirectory,"install_TIDDIT.sh"),SVenXDirectory)]
tmp=subprocess.check_output(command,shell = True)
template=template.replace("{TIDDIT_path}", "\'{}\'".format(os.path.join(SVenXDirectory,"TIDDIT/bin/TIDDIT")) )

# SV - CNVnator
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