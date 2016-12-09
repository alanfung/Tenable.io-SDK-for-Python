class BaseTest(object):

    def setup_method(self, method):
        print "\n%s:%s" % (type(self).__name__, method.__name__)

    def teardown_method(self, method):
        pass
