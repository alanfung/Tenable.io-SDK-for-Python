# Nessus Python SDK
Nessus Python SDK

### Configuration
Access key and secret key are needed to authenticate with the [Tenable Cloud API]. There are three ways to configure the `NessusClient` with the keys.

##### INI File
A `nessus.ini` can be created in the working directory. See `nessus.ini.example` on what it should look like.

#### `NessusClient` Constructor Arguments
```python
NessusClient(access_key='YOUR_ACCESS_KEY', secret_key='YOUR_SECRET_KEY')
```

#### Environment Variables
NessusClient looks for the environment variables `NESSUS_ACCESS_KEY` and `NESSUS_SECRET_KEY`.

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
