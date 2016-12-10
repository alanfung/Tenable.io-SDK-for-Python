from os import environ
import six

if six.PY34:
    import configparser
else:
    import ConfigParser as configparser

base_config = {
    'endpoint': environ.get('NESSUS_ENDPOINT', 'https://cloud.tenable.com/'),
    'access_key': environ.get('NESSUS_ACCESS_KEY'),
    'secret_key': environ.get('NESSUS_SECRET_KEY'),
}

# Read nessus.ini config. Default to environment variables if exist.
config = configparser.SafeConfigParser(base_config)
config.add_section('nessus')
config.read('nessus.ini')


class NessusConfig(object):

    @staticmethod
    def get(key):
        return config.get('nessus', key)
