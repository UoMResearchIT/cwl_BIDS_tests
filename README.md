# Tests to figure out how to use CWL in a complex directory structure

CWL is designed to work with a flat directory structure. Input paths are always[^1]
relative to the *inputs_object* (JSON or YAML file). All outputs are written to the
same folder, which _can_ be configured with `--outdir`.

The [BIDS standard](https://bids-standard.github.io/bids-starter-kit/folders_and_files/folders.html) 
requires a complex directory structure, with file and folder names that change
with subject, session, and modality.

[^1]: CWLTool has a `--basedir` option that (you'd guess) would allow you to specify the base directory for relative paths. 
It either doesn't work, or does something different:
[document what --basedir does #278](https://github.com/common-workflow-language/cwltool/issues/278) (open since 2017), and
["--basedir" option is not working #668](https://github.com/common-workflow-language/cwltool/issues/668) (open since 2018)

## Location of *inputs_object*

The inputs file can either be placed close to the data (shorter paths),
or at the output directory (skip the `--output` argument, allow *inputs_object* to become an executable that runs the pipeline).

```bash
# inputs_object (dummy.yml) close to data
cwltool --outdir derivatives/sub-01/dummy \
  code/dummy.cwl rawdata/sub-01/ses-01/dummy.yml

# inputs_object (dummy.yml) at output directory
cwltool derivatives/sub-01/dummy/dummy.yml code/dummy.cwl

# with cwl:tool, shebang, and chmod +x (see notes)
./derivatives/sub-01/dummy/dummy.yml
```

#### Notes

- Adding `cwl:tool: path/to/workflow.cwl` allows linking the *cwl_document* (workflow file) to the *inputs_object*, and `cwltool` to be called with a single argument.

- The *inputs_object* can be made executable by adding a shebang and making it executable with `chmod +x dummy.yml`.

- `#!/usr/bin/env cwl-runner` requires `cwl-runner` to be set as an alias for `cwltool` in the shell.
e.g. `ln -sr .venv/bin/cwltool .venv/bin/cwl-runner` for a virtual environment.

## Passing input files by name

An option to preserve short data paths is to pass them as strings, along with
a base directory, e.g. `derivatives/sub-02/dummy/dummy_from_folder.yml`

This also allows globbing inputs from wildcard patterns (see [below](#globbing-input-names)).

#### Cons:

-  Requires an additional workflow step to copy the input files to the working directory
-  Probably goes against the *spirit* of CWL (explicit types and input names)

## Simplifying the *inputs_object*

It might be desirable to hard-code the data folder structure into the CWL workflow, 
and pass only the base directory as input.

The suggested mechanism to do this is a *Dirent listing* as `InitialWorkDirRequirement`:

```yaml
requirements:
  LoadListingRequirement:
    loadListing: shallow_listing
  InitialWorkDirRequirement:
    listing:
      - entry: $(inputs.basedir)
        entryname: basedir
      - entry: $(inputs.some_file)
        entryname: sub/path/to/some_file
inputs:
  basedir: Directory
  some_file: File
```
However, **this doesn't work for array inputs**. An alternative is to pass files
indirectly by name/pattern (see [below](#globbing-input-names)).

## Dealing with changing file names

The examples above are hard-coded to work with a single session. To work with multiple data-sets,
the *inputs_object* would have to be created for each session (e.g. from a template), 
or the workflow modified to accept wildcards/configurable file names.

### *inputs_object* templates (TODO)

Input files could be e.g. Jinja-parsed instances of a template, `code/dummy_template.yml`,
copied to either the data directory or the output directory.

**Pros**: inputs object as provenance record?

**Cons**: copies everywhere, one config per session, requires external templating engine

### Globbing input names

Addressing input files by name allows for wildcard-patterns to be used
in the *inputs_object*. This adds flexibility, but requires an extra worflow step
for each input.

E.g. `code/dummy_glob_inputs.cwl` encodes the inner data structure as part of the workflow,
in the form of file-name patterns parsed by `code/glob_inputs.cwl`. The resulting input
file `derivatives/sub-03/dummy/dummy_glob_inputs.yml` points only to the base directory
and workflow file.

**Pros**: potential for single workflow config (scatter over Directories), simpler *inputs_object*

**Cons**: extra step for each input, more complex workflow

### Snakemake workflow for CWL tools? (TODO)

The BIDS specification seems custom-tailored for *Snakemake*, which is meant to
work with wildcard-based file names. It should be possible to use Snakemake to
run CWL tools, or just drop CWL altogether.