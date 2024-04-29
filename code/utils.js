
// Return flat lists of all paths and objects in a directory tree
// { pathList, objectList } = flatListing(basedir);
function flatListing(basedir) {
  var pathList = [];
  var objectList = [];

  function traverse(subdir, base) {

    if (subdir.class !== 'Directory') {
      return;
    }
    
    subdir.listing.forEach(function(item) {
      var path = base + "/" + item.basename;
      pathList.push(path);
      objectList.push(item);

      if (subdir.class === 'Directory') {
        traverse(item, path);
      }
    });
  }
  traverse(basedir, '');
  return { pathList: pathList, objectList: objectList };
}

// Jinja-like template replacement
// result = replaceTokens("{{foo}}_{{bar}}", { foo: 1, bar: "B"});
function replaceTokens(template, replacements) {

  var regex = /{{\s*(\w+)\s*}}/g;

  return template.replace(regex, function(match, key) {
    if (key in replacements) {
      return replacements[key];
    } else {
      return match;
    }
  });
}
