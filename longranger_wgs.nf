#!/usr/bin/env nextflow

params.fastq = ""
params.folder = ""
params.sample = ""

if (params.folder) {
	String character = "/*";
	String folder_path = params.fastq;
	sample_path =folder_path+character;
	//System.out.println(otherString);
	tenX_path = Channel.fromPath(sample_path, type: 'dir') // .map { row[] } // subscribe { map -> println "${map[0]} - ${map[1]}" }
	//tenX_path.subscribe {println "${it}"}
}

if (params.sample) {
	tenX_path = params.fastq
}


// Longranger wgs will generate bam and vcf files. If dry run; it uses samples that already exist (only works on vanja@milou.uppmax.uu.se) 
if (params.wgs) {
	process longRanger_wgs  {
		publishDir params.workingDir, mode: "copy", overwrite: true
		errorStrategy 'ignore' 

		input:
		val path from tenX_path

		output:
		set "bam", "dels_vcf", "large_svs_vcf", "phased_variants_vcf" into bam_vcf_wgs 

		script:
  
  		if (!params.dry_run){

		"""
			longranger wgs --id=${params.id} --reference=${params.ref} --fastqs=$path  
			mv ${params.id}/outs/phased_possorted_bam.bam ./bam
			mv ${params.id}/outs/dels.vcf.gz ./dels_vcf
			mv ${params.id}/outs/large_svs.vcf.gz ./large_svs_vcf
			mv ${params.id}/outs/phased_variants.vcf.gz ./phased_variants_vcf	
		"""
	
		}else{
		"""
			ln -s ${params.wgs_result} ${params.id} 
			cp ${params.id}/outs/phased_possorted_bam.bam ./bam
			cp ${params.id}/outs/dels.vcf.gz ./dels_vcf
			cp ${params.id}/outs/large_svs.vcf.gz ./large_svs_vcf
			cp ${params.id}/outs/phased_variants.vcf.gz ./phased_variants_vcf
		"""
		}
	}
}