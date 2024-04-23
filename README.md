# Tests to figure out how to use CWL in a complex directory structure

## Wait until CWLTool gets fixed

[**document what --basedir does #278**](https://github.com/common-workflow-language/cwltool/issues/278) (open since 2017)
[**"--basedir" option is not working #668**](https://github.com/common-workflow-language/cwltool/issues/668) (open since 2018)

## Symlink config files

Place the input file where the relative paths make sense. e.g.:

```bash
cd study
ln -sr code/dummy.yml rawdata/sub-01/ses-01/
cwltool --outdir derivatives/sub-01/dummy code/dummy.cwl rawdata/sub-01/ses-01/dummy.yml
```

**PROS**: simple, developer-friendly
**CONS**: file copies everywhere, one config per session, input file is not configurable

## TODO: Config file templates

Copy Jinja-parsed instances of the input file to the working directory.

**PROS**: provenance record
**CONS**: file copies everywhere, one config per session, requires external templating engine

## Flatten Inputs

Use `relpaths2files.cwl` to stage files in a complex tree to working directory.

```bash
cwltool --outdir derivatives/sub-02/dummy code/wrapped_dummy.cwl code/wrapped_dummy.yml
```

**PROS**: potential for workflow config (scatter over Directories?), might need
  to be modified to use name globbing
**CONS**: clunky, hacky

## TODO: Snakemake workflow for CWL tools?