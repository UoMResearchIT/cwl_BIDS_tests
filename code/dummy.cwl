cwlVersion: v1.2
class: CommandLineTool
baseCommand: ls

stdout: dummy.out

inputs:
  files: File[]
outputs:
  log:
    type: File
    outputBinding:
      glob: dummy.out