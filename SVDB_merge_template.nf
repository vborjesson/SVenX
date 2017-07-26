

input_files = @@@@@

process SVDB_merge {
    publishDir "${params.working_dir}", mode: 'copy', overwrite: true
    errorStrategy 'ignore'      
        
    input:
    

    set ID,  ¤¤¤¤¤  from input_files                            (.replace)

    output:
    
    script:
    """
        ${TIDDIT_exec_file} --sv -b ${bam} -p ${params.TIDDIT_pairs} -q ${params.TIDDIT_q} -o ${ID}_TIDDIT
        rm *.tab
    """
    }
