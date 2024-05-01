#!/usr/bin/env python

"""
Command-line tool for creating instances of input/config files for BIDS
workflows, based on a template.

Renders a Jinja2 TEMPLATE file, replacing tokens {{sub}}, {{ses}},
{{name}}, and {{basedir}} and writing the result to a TARGET file

By default, the TARGET is 'derivatives/SUB/SES/NAME', where NAME is the
TEMPLATE base-name (with .jinja* extension removed, if existing).
The parent TARGET directory will be created if it does not exist.

Paths for TEMPLATE and TARGET can be relative to BASEDIR. For consistency,
the {{basedir}} token should be used in the TEMPLATE file for any relative
paths, as these may change depending on TARGET.
"""

import argparse
import jinja2
import os

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--sub", required=True, help="Subject label ('sub-' prefix will be added if missing)")
parser.add_argument("--ses", required=True, help="Session label ('ses-' prefix will be added if missing)")
parser.add_argument("--template", required=True, help="Input-object template")
parser.add_argument("--target", required=False, default="derivatives/{{sub}}/{{ses}}/{{name}}",
                    help="Target file path (Jinja2 template string), default: '%(default)s'")
parser.add_argument("--name", required=False, default=None,
                    help="Workflow name (default: base-name of TEMPLATE, without .jinja* extension)")
parser.add_argument("--basedir", required=False, default=None, help="Base directory for relative paths")

# remove whitespace from Jinja2 blocks
JINJA_OPTS = {"trim_blocks": True, "lstrip_blocks": True}

def create_instance(template, sub, ses, target = parser.get_default('target'), name = None, basedir = None):

  # Extract the workflow name from the template, if missing
  if name is None:
    name = os.path.basename(template)
    if "jinja" in os.path.splitext(name)[1].lower():
      name = os.path.splitext(name)[0]

  # Parse replacement tokens
  if not sub.startswith("sub-"):
    sub = "sub-" + sub
  if not ses.startswith("ses-"):
    ses = "ses-" + ses

  if basedir is None:
    basedir = "."

  tokens = {
    "sub": sub,
    "ses": ses,
    "name": name,
    "basedir": basedir
  }

  # Parse target, basedir, and template paths
  target = jinja2.Template(target, **JINJA_OPTS).render(tokens)

  basedir = abs_path(basedir)
  template = abs_path(template, basedir)
  target = abs_path(target, basedir)

  # Make sure the replacement `basedir` token is relative to target
  target_dir = os.path.dirname(target)
  tokens["basedir"] = os.path.relpath(basedir, target_dir)

  # Render the template
  with open(template, "r") as f:
    template_str = f.read()

  instance = jinja2.Template(template_str, **JINJA_OPTS).render(tokens)

  os.makedirs(target_dir, exist_ok=True)
  with open(target, "w") as f:
    f.write(instance)

  print("Created instance at", target)
  return target

def abs_path(path, basedir = ""):
  path = os.path.expanduser(os.path.expandvars(path))
  if not os.path.isabs(path):
      path = os.path.abspath(os.path.join(basedir, path))
  return path

if __name__ == "__main__":
  args = parser.parse_args()
  create_instance(**args)

