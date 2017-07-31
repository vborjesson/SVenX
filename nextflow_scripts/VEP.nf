

process VEP_annotation {
	publishDir params.workingDir, mode: "copy", overwrite: true
	errorStrategy 'ignore' 

	input:
	set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from wgs_outs_vep

	output:
	file "${ID}_dels_VEP.vcf" into VEP_output

	script:
	"""
	variant_effect_predictor.pl --cache -i ${dels_vcf} -o ${dels_vcf}_tmp --format vcf --vcf --port 3337 --offline --force_overwrite                    
	mv ${dels_vcf}_tmp ${ID}_dels_VEP.vcf
	"""
}
