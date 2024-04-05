cwlVersion: v1.2
class: ExpressionTool
label: Take a directory and a list of relative file paths and return a file array

requirements:
  InlineJavascriptRequirement: {}

inputs:
  relpaths: string[]
  basedir: Directory

outputs:
  files: File[]
  basedir: Directory

expression: |
  ${
    var files = [];
    for (var i = 0; i < inputs.relpaths.length; i++) {
      files.push({
        class: "File",
        location: inputs.basedir.location + "/" + inputs.relpaths[i]
      });
    }
    return {"files": files, "basedir": inputs.basedir};
  }

