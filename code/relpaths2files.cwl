cwlVersion: v1.2
class: CommandLineTool
label: return a file array from a directory and a list of relative file paths 

requirements:
  - class: InlineJavascriptRequirement
    expressionLib:
      - |
        function filelist(relpaths, basedir) {
          var files = [];
          for (var i = 0; i < relpaths.length; i++) {
            files.push({
              class: "File",
              location: basedir.location + "/" + relpaths[i]
            });
          }
          return files;
        }
  - class: InitialWorkDirRequirement
    listing:
      - $(filelist(inputs.relpaths, inputs.basedir))

baseCommand: echo
# stdout: out.log

inputs:
  relpaths: string[]
  basedir: Directory

outputs:
  files: 
    type: File[]
    outputBinding:
      glob: "*"
  # log: 
  #   type: File
  #   outputBinding:
  #     glob: out.log
