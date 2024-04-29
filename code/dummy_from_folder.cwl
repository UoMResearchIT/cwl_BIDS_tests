cwlVersion: v1.2
class: Workflow
label: 

inputs:
  basedir: Directory
  files: string[]

outputs: 
  log:
    type: File
    outputSource: dummy/log

steps:
  from_folder:
    run: from_folder.cwl
    in:
      basedir: basedir
      relpaths: files
    out: [files]
  dummy:
    run: dummy.cwl
    in:
       files: from_folder/files
    out: [log]