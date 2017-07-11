
import os
import subprocess

programDirectory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(programDirectory,"SVenX_nf.config"), 'r') as myfile:
    template=myfile.read()

print "Enter standard output directory"
selection=raw_input()
template=template.replace("{working_dir}", "\'{}\'".format(selection) )

print "Set the path to the reference genome hg 19"
selection=raw_input()
template=template.replace("{ref_genome}", "\'{}\'".format(selection) )

print "Set the path to the reference genome hg 19"
selection=raw_input()
template=template.replace("{ref_genome}", "\'{}\'".format(selection) )


print "installing and setting up TIDDIT"
command=["{} {}".format(os.path.join(programDirectory,"internal_scripts/install_FT.sh"),programDirectory)]
tmp=subprocess.check_output(command,shell = True)
template=template.replace("{TIDDIT_path}", "\'{}\'".format(os.path.join(programDirectory,"TIDDIT/bin/TIDDIT")) )

print "Setting up manta"
print "Set the manta configManta path, the path is set to configManta if left blank"
selection=raw_input()
if selection == "":
    selection = "configManta.py"
template=template.replace("{configManta}", "\'{}\'".format(selection) )

