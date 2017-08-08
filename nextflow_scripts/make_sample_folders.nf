
process make_folder {
		publishDir params.workingDir, mode: "copy", overwrite: true
		errorStrategy 'ignore' 

		input:
		set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from wgs_outs_make_folders

		output:
		file "outs" into make_folders 

		script:
		"""
		cd ${params.workingDir}
		mkdir ${ID}_outs 
		mv ${ID}* ./${ID}_outs
		"""
}

