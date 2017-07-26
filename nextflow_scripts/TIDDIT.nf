
//------------------------------TIDDIT----------------------------------    

TIDDIT_exec_file = file( "${params.TIDDIT_path}" )

process TIDDIT {
    publishDir "${params.workingDir}", mode: 'copy', overwrite: true
    errorStrategy 'ignore'      
        //tag { bam_file }
    
        //cpus 1
        
    input:
        //set ID,  file(bam_file), file(bai_file) from TIDDIT_bam
    set ID, bam, dels_vcf, large_svs_vcf, phased_variants_vcf from wgs_outs_TIDDIT
    
    output:
    set ID, "${ID}_TIDDIT.vcf" into TIDDIT_output
    
    script:
    """
        ${TIDDIT_exec_file} --sv -b ${bam} -p ${params.TIDDIT_pairs} -q ${params.TIDDIT_q} -o ${ID}_TIDDIT
        rm *.tab
    """
    }