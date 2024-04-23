cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs:
  basedir: Directory
  files: string[]

outputs: 
  log:
    type: File
    outputSource: dummy/log

steps:
  relpaths2files:
    run: relpaths2files.cwl
    in:
      basedir: basedir
      relpaths: files
    out: [files]
  dummy:
    run: dummy.cwl
    in:
       files: relpaths2files/files
    out: [log]