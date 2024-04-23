cwlVersion: v1.2
class: CommandLineTool
baseCommand: ls

stdout: dummy.out

inputs:
  files:
    type: File[]
    inputBinding: {}
outputs:
  log:
    type: File
    outputBinding:
      glob: dummy.out