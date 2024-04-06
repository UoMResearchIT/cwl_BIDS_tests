cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs:
  basedir: Directory
  files: string[]

outputs: 
  output:
    type: File
    outputSource: foo/output

steps:
  relpaths2files:
    run: relpaths2files.cwl
    in:
      basedir: basedir
      relpaths: files
    out: [files]
  foo:
    run: foo.cwl
    in:
       files: relpaths2files/files
    out: [output]