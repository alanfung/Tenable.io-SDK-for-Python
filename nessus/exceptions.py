class NessusException(Exception):

    def __init__(self, response):
        self.response = response

    def __str__(self):
        return self.response.text


class NessusRetryableException(NessusException):
    pass
