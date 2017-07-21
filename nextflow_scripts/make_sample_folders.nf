
process make_folder {
		publishDir params.workingDir, mode: "copy", overwrite: true
		errorStrategy 'ignore' 

		input:
		set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from bam_vcf_wgs

		output:
		file "${ID}_dels_annotated_VEP.vcf" into VEP_files 

		script:
		"""
		cd ${params.workingDir}
		ls -l ${ID}*_bam | while read line; do rename 's/\_bam/\.bam/' $line; done
		ls -l ${ID}*_vcf | while read line; do rename 's/\_vcf/\.vcf/' $line; done
		mkdir ${ID}_outs 
		mv ${ID}* ./${ID}_outs
		"""
}

