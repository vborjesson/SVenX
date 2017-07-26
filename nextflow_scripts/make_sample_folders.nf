
process make_folder {
		publishDir params.workingDir, mode: "copy", overwrite: true
		errorStrategy 'ignore' 

		input:


		output:
		file "outs" into make_folders 

		script:
		"""
		cd ${params.workingDir}
		mkdir ${ID}_outs 
		mv ${ID}* ./${ID}_outs
		"""
}

