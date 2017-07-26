
//------------------------------CNVnator----------------------------------
    
CNVnator_exec_file=params.CNVnator_path
CNVnator2vcf=params.CNVnator2vcf_path
//ROOT=file("${params.thisroot_path}")
CNVnator_reference_dir=file("${params.CNVnator_reference_dir_path}")


process CNVnator {
        publishDir "${params.workingDir}", mode: 'copy', overwrite: true
        errorStrategy 'ignore'
        //tag { bam_file }       

        //cpus 1

        input:
        //set ID,  file(bam_file), file(bai_file) from CNVnator_bam
        set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from wgs_outs_CNVnator

        output: 
        set ID, "${bam.name}_CNVnator.vcf" into CNVnator_output
            
        script:
        """
        ${CNVnator_exec_file} -root cnvnator.root -tree ${bam}
        ${CNVnator_exec_file} -root cnvnator.root -his ${params.CNVnator_bin_size} -d ${CNVnator_reference_dir}
        ${CNVnator_exec_file} -root cnvnator.root -stat ${params.CNVnator_bin_size} >> cnvnator.log
        ${CNVnator_exec_file} -root cnvnator.root -partition ${params.CNVnator_bin_size}
        ${CNVnator_exec_file} -root cnvnator.root -call ${params.CNVnator_bin_size} > ${bam.name}_CNVnator.out
        ${CNVnator2vcf} ${bam.name}_CNVnator.out >  ${bam.name}_CNVnator.vcf
        rm cnvnator.root
        """
    }