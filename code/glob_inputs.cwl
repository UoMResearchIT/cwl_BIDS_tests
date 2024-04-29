cwlVersion: v1.2
class: ExpressionTool
label: Glob files and subdirectories from a base directory
doc: |
  Recognizes both ** and * wildcards in the patterns.
  TODO: Add support for user-provided regex patterns.

requirements:
  LoadListingRequirement: {loadListing: "deep_listing"}
  InlineJavascriptRequirement:
    expressionLib:
    - { $include: utils.js }

inputs:
  patterns: string[]
  basedir: Directory

outputs:
  matches: 
    type:
      - type: array
        items:
          - File
          - Directory

expression: |
  ${
    var flatList = flatListing(inputs.basedir);
    var pathList = flatList.pathList;
    var objectList = flatList.objectList;

    var arr = [];
    inputs.patterns.forEach(function (pattern) {

      if (pattern.startsWith("./")) {
        pattern = pattern.substring(2);
      }

      if (pattern.includes("*")) {
        
        pattern = pattern.replace(/\*\*/g, ".*");
        pattern = pattern.replace(/(?<!\.)\*/g, "[^/]*");
        pattern = new RegExp(pattern);

        pathList.forEach(function (path, index) {
          if (pattern.test(path)) {
            arr.push(objectList[index]);
          }
        });

      } else {

        pathList.forEach(function (path, index) {
          if (path === pattern) {
            arr.push(objectList[index]);
          }
        });
      }
    });
    return {"matches": arr};
  }