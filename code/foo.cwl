cwlVersion: v1.2
class: CommandLineTool
baseCommand: ls

stdout: foo.out

inputs:
  files:
    type: File[]
    inputBinding: {}
outputs:
  output:
    type: File
    outputBinding:
      glob: foo.out