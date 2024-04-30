#!/usr/bin/env python

"""
Command-line tool for creating instances of input/config files for BIDS
workflows, based on a template.

Renders a Jinja2 TEMPLATE file, replacing tokens {{sub}}, {{ses}},
{{name}}, and {{basedir}} and writing the result to TARGET/NAME.EXT

By default, the TARGET directory is 'derivatives/SUB/NAME/', and NAME is
extracted from the template's `cwl:tool: path/to/NAME.cwl` basename. The
TARGET directory will be created if it does not exist. The file extension
EXT is preserved from the template.

Paths for TEMPLATE and TARGET can be relative to BASEDIR. For consistency,
the {{basedir}} token should be used in the TEMPLATE file for any relative
paths, as these may change depending on TARGET.
"""

import argparse
import jinja2
import os
import re

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--sub", required=True, help="Subject label ('sub-' prefix will be added if missing)")
parser.add_argument("--ses", required=True, help="Session label ('ses-' prefix will be added if missing)")
parser.add_argument("--template", required=True, help="Input-object template")
parser.add_argument("--target", required=False, default="derivatives/{{sub}}/{{name}}/",
                    help="Target directory (Jinja2 template string), default: '%(default)s'")
parser.add_argument("--name", required=False, default=None,
                    help="Workflow name, extracted from the template's `cwl:tool` basename, if missing")
parser.add_argument("--basedir", required=False, default=None, help="Base directory for relative paths")

def create_instance(template, sub, ses, target = parser.get_default('target'), name = None, basedir = None):

  if basedir:
    os.chdir(basedir)
  basedir = os.getcwd()

  # Load the template file
  with open(template, "r") as f:
    template_str = f.read()

  # Extract the workflow name from the template, if missing
  if name is None:
    match = re.search(r'cwl:tool:.*/(.*)\.cwl', template_str)
    if match is None:
      raise ValueError("Could not extract workflow name from template")
    else:
      name = match.group(1)

  if not sub.startswith("sub-"):
    sub = "sub-" + sub
  if not ses.startswith("ses-"):
    ses = "ses-" + ses

  tokens = {
    "sub": sub,
    "ses": ses,
    "name": name,
    "basedir": basedir
  }

  # Create the target directory
  target_dir = jinja2.Template(target).render(tokens)
  os.makedirs(target_dir, exist_ok=True)

  target_dir = os.path.abspath(target_dir)
  tokens["basedir"] = os.path.relpath(basedir, target_dir)
  
  # Render the template
  instance = jinja2.Template(template_str).render(tokens)

  # Write the instance to a file
  ext = os.path.splitext(template)[1]
  out_file = os.path.join(target_dir, name + ext)
  with open(out_file, "w") as f:
    f.write(instance)

  print("Created instance at", out_file)
  return out_file

if __name__ == "__main__":
  args = parser.parse_args()
  create_instance(args.template, args.sub, args.ses, args.target, args.name, args.basedir)

