import six

if six.PY34:
    import configparser
else:
    import ConfigParser as configparser

base_config = {
}

# Read nessus.ini config. Default to environment variables if exist.
config = configparser.SafeConfigParser(base_config)
config.add_section('nessus-test')
config.read('nessus.ini')


class NessusTestConfig(object):

    @staticmethod
    def get(key):
        return config.get('nessus-test', key)
