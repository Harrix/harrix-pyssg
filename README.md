# Harrix-Static-Site-Generator

**In development.**

A simple static website generator in Python.

## Install

Pip:

```console
pip install harrix-pylib
```

Pipenv:

```console
pip update harrix-pylib
```

## Update

Pip:

```console
pipenv install harrix-pylib
```

Pipenv:

```console
pipenv update harrix-pylib
```

## Development

If you don't have [pipenv](https://pipenv.pypa.io/en/latest/) installed, then you can install it via the commands:

```py
python -m pip install virtualenv
python -m pip install pipenv
```

Installing packages by file `Pipfile`:

```py
pipenv install --dev
pipenv shell
```

Generate docs:

```console
pdoc --docformat="google" src\harrixpyssg\
```
