class NessusException(Exception):
    pass


class NessusApiException(NessusException):

    def __init__(self, response):
        self.response = response

    def __str__(self):
        return self.response.text


class NessusRetryableApiException(NessusApiException):
    pass
