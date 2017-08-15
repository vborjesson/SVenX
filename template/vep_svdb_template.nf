
//----------------------VEP - SVDB query ------------------------------

process VEP {
	publishDir params.workingDir, mode: "copy", overwrite: true
	errorStrategy 'ignore' 

	input:
	¤¤¤¤

	output:
	set ID, "${ID}_VEP.vcf" into VEP_out

	script:
	"""
	variant_effect_predictor.pl --cache -i &&&& -o ${ID}_tmp --format vcf --vcf --port 3337 --offline --force_overwrite                    
	mv ${ID}_tmp ${ID}_VEP.vcf
	"""
}

process svdb_query {
	publishDir params.workingDir, mode: "copy", overwrite: true
	errorStrategy 'ignore' 

	input:
	set ID, vep_vcf from VEP_out

	output:
	set ID, "${ID}_filtered.vcf" into filtered_vcf

	script:
	"""
	svdb --query --query_vcf ${vep_vcf} --db ${params.svdb_database} > ${ID}_SVDB_query.vcf
	cat ${ID}_SVDB_query.vcf | grep PASS > ${ID}_filtered.vcf
	"""
}


