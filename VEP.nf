

if (params.wgs) { 
	process VEP_annotation 	{
		publishDir params.workingDir, mode: "copy", overwrite: true
		errorStrategy 'ignore' 

		input:
		set bam, dels_vcf, large_svs_vcf, phased_variants_vcf from bam_vcf_wgs

		output:
		file "dels_annotated_VEP.vcf" into VEP_files 

		script:
		"""
		variant_effect_predictor.pl --cache -i ${dels_vcf} -o ${dels_vcf}.tmp --format vcf --vcf --port 3337 --offline --force_overwrite                    
    	mv ${dels_vcf}.tmp dels_annotated_VEP.vcf
		"""
	}
}

