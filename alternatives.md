## Wait until CWLTool gets fixed

[**document what --basedir does #278**](https://github.com/common-workflow-language/cwltool/issues/278) (open since 2017)
[**"--basedir" option is not working #668**](https://github.com/common-workflow-language/cwltool/issues/668) (open since 2018)

## Symlink config files

Place the input file where the relative paths make sense.

```bash
cd study
ln -sr code/foo.yml rawdata/sub-01/ses-01/
cwltool --outdir derivatives/sub-01/foo code/foo.cwl rawdata/sub-01/ses-01/foo.yml
```

## 