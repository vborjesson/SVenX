
combined_first = ©©©©©
combined_final = @@@@@

process SVDB_merge {
    publishDir params.workingDir, mode: 'copy', overwrite: true
    errorStrategy 'ignore'      
        
    input:
    set ID,  ¤¤¤¤¤  from combined_final  

    output:
    set ID, "${ID}_merged_callers.vcf" into SVDB_merge_outout

    script:
    """
        svdb --merge --vcf £££££ > ${ID}_merged_callers.vcf 
    """
    }

