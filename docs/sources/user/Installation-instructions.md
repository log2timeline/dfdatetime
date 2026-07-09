# Installation instructions

## pip

**Note that using pip outside virtualenv is not recommended since it ignores
your systems package manager. If you aren't comfortable debugging package
installation issues use virtualenv.**

Create and activate a virtualenv:

```bash
virtualenv dfdatetime_venv
cd dfdatetime_venv
source ./bin/activate
```

Upgrade pip and install dfDateTime dependencies:

```bash
pip install --upgrade pip
pip install dfdatetime
```

To deactivate the virtualenv run:

```bash
deactivate
```
