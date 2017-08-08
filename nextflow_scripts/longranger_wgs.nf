#!/usr/bin/env nextflow

params.fastq = ""
params.folder = ""
params.sample = ""





// Channel all samples from folder in order to parallelize longranger
if (params.folder) {
	String character = "/*";
	String folder_path = params.fastq;
	sample_path =folder_path+character;
	//System.out.println(otherString);
	tenX_path = Channel.fromPath(sample_path, type: 'dir').map {path -> tuple(path.name, path)}
}

// If just one sample; no channels are needed
if (params.sample) {
	String character = "/*";
	String folder_path = params.fastq;
	sample_path =folder_path;
	//System.out.println(otherString);
	tenX_path = Channel.fromPath(sample_path, type: 'dir').map {path -> tuple(path.name, path)}
}

// tenX_path = params.fastq


// Longranger wgs will generate bam and vcf files. If dry run; it uses samples that already exist (only works on vanja@milou.uppmax.uu.se) 
if (params.wgs) {
	process longRanger_wgs  {
		publishDir params.workingDir, mode: "copy", overwrite: true
		errorStrategy 'ignore' 

		input:
		set ID, path from tenX_path

		output:
		set ID, "${ID}.bam", "${ID}_dels.vcf.gz", "${ID}_large_svs.vcf", "${ID}_phased_variants.vcf.gz" into wgs_outs 

		script:
  
  		if (!params.dry_run){

		"""
			longranger wgs --id=${ID} --reference=${params.ref} --fastqs=$path  
			mv ${ID}/outs/dels.vcf.gz ./${ID}_dels.vcf
			mv ${ID}/outs/phased_possorted_bam.bam ./${ID}.bam
			mv ${ID}/outs/dels.vcf.gz ./${ID}_dels.vcf.gz
			mv ${ID}/outs/large_svs.vcf.gz ./${ID}_large_svs.vcf.gz
			mv ${ID}/outs/phased_variants.vcf.gz ./${ID}_phased_variants.vcf.gz	
		"""
	
		}else{

		"""
			ln -s ${params.wgs_result} ${ID} 
			cp ${ID}/outs/phased_possorted_bam.bam ./${ID}.bam
			cp ${ID}/outs/dels.vcf.gz ./${ID}_dels.vcf.gz
			cp ${ID}/outs/large_svs.vcf.gz ./${ID}_large_svs.vcf.gz
			gunzip ./${ID}_large_svs.vcf.gz
			cp ${ID}/outs/phased_variants.vcf.gz ./${ID}_phased_variants.vcf.gz
		"""

		}
	}
}

wgs_outs.into {
  wgs_outs_vep
  wgs_outs_TIDDIT
  wgs_outs_CNVnator
  wgs_outs_SVDB 
  wgs_outs_make_folders
}