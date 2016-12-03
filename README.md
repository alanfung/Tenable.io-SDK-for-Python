# Nessus Python SDK

Nessus Python SDK

### Python Version

2.7, 3.5

### Development

It is recommend to use `virtualenv` to setup an isolated local environment.
```sh
$ virtualenv .venv
# To use a different python bin (i.e. python3).
$ virtualenv .venv3 -p $(which python3)
# To active the virtualenv
$ source ./venv/bin/activate
```

Install dependencies.
```sh
$ pip install -r ./requirements.txt
```

### Run Tests

```sh
$ py.test
```
