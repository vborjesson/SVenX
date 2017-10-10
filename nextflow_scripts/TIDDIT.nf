
//------------------------------TIDDIT----------------------------------    

TIDDIT_exec_file = file( "${params.TIDDIT_path}" )

process TIDDIT {
    publishDir "${params.workingDir}", mode: 'copy', overwrite: true
    errorStrategy 'ignore'      
        //tag { bam_file }
    
        // cpus 1
        
    input:

    set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from wgs_outs_TIDDIT
    
    output:
    set ID, "${ID}_TIDDIT.vcf", "${ID}_TIDDIT.tab" into TIDDIT_output
    
    script:
    """
        ${TIDDIT_exec_file} --sv -b ${bam} -p ${params.TIDDIT_pairs} -q ${params.TIDDIT_q} -o ${ID}_TIDDIT
    """
    }

    // outputs can only be used once as input in a new process, therefor we copy them into several identical outputs. 
    TIDDIT_output.into {
    TIDDIT_output_svdbmerge
    TIDDIT_output_GlenX
}