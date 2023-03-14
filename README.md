# Pysira
![Tests](https://github.com/hmiladhia/pysira/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/hmiladhia/pysira/branch/main/graph/badge.svg)](https://codecov.io/gh/hmiladhia/nbmanips)

CLI tool to export [jsonresume](https://jsonresume.org/) files to different formats (html, tex, pdf, ...) and different languages.


## Example

```bash
sira export -t stackoverflow examples/resume.json -o examples/out/stackoverflow
```

## Help

```
>> sira export --help
Usage: sira export [OPTIONS] [RESUME_PATH]

Options:
  -o, --output TEXT
  -t, --theme TEXT
  -l, --language TEXT
  -op, --options TEXT
  -f, --format TEXT
  -w, --work INTEGER
  -p, --projects INTEGER
  -s, --skills INTEGER
  -c, --certificates INTEGER
  -a, --summary, --about / -na, --no-summary, --no-about
  -y, --yaml
  --help                          Show this message and exit.

```
