
# Open Datalake - Connectors

s3pypi dist/* --bucket pypi.joffreybvn.be --profile private --put-root-index -f -v

## Install libraries

TLDR: Always add `--extra-index-url https://pypi.joffreybvn.be` to you pip command.

### Installing `open-connector`
With a pip command:
```shell
pip install open-connector --extra-index-url https://pypi.joffreybvn.be
```