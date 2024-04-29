cwlVersion: v1.2
class: Workflow

inputs:
  basedir: Directory
  files: 
    type: string[]
    default: 
      - "**_inv-400_IRT1.nii.gz"
      - "**_inv-800_IRT1.nii.gz"
      - "**_inv-1000_IRT1.nii.gz"

outputs: 
  log:
    type: File
    outputSource: dummy/log

steps:
  glob_inputs:
    run: glob_inputs.cwl
    in:
      basedir: basedir
      patterns: files
    out: [matches]
  dummy:
    run: dummy.cwl
    in:
       files: glob_inputs/matches
    out: [log]