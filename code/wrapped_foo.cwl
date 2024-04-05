cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}
  LoadListingRequirement:
    loadListing: deep_listing
  InitialWorkDirRequirement:
    listing:
      - entryname: basedir
        entry: $(inputs.basedir)

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