# Tests to figure out how to use CWL in a complex directory structure

## Wait until CWLTool gets fixed

[**document what --basedir does #278**](https://github.com/common-workflow-language/cwltool/issues/278) (open since 2017)
[**"--basedir" option is not working #668**](https://github.com/common-workflow-language/cwltool/issues/668) (open since 2018)

## Symlink config files

Place the input file where the relative paths make sense. e.g.:

```bash
cd study
ln -sr code/foo.yml rawdata/sub-01/ses-01/
cwltool --outdir derivatives/sub-01/foo code/foo.cwl rawdata/sub-01/ses-01/foo.yml
```

**PROS**: simple, developer-friendly
**CONS**: file copies everywhere, , one config per session, input file is not configurable

## TODO: Config file templates

Copy Jinja-parsed instances of the input file to the working directory.

**PROS**: provenance record
**CONS**: file copies everywhere, one config per session, requires external templating engine

## Flatten Inputs

Use `relpaths2files.cwl` to stage files in a complex tree to working directory.

```bash
cwltool --outdir derivatives/sub-02/foo wrapped_foo.cwl wrapped_foo.yml
```

**PROS**: potential for workflow config (scatter over Directories?), might need
  to be modified to use name globbing
**CONS**: clunky, hacky

## TODO: Snakemake workflow for CWL tools?