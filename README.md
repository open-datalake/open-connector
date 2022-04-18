
# Open Datalake - Connectors

s3pypi dist/* --bucket pypi.joffreybvn.be --profile private --put-root-index -f -v

## Install libraries

Always add `--extra-index-url https://pypi.joffreybvn.be` to you pip command.
Alternatively, you can also add this parameter to your `requirements.txt`.

Example:
```shell
open-connector
source-s3
destination-s3
--extra-index-url=https://pypi.joffreybvn.be
```

### Installing `open-connector`
With a pip command:
```shell
pip install open-connector --extra-index-url https://pypi.joffreybvn.be
```