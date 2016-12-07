class BaseResource(object):

    def __init__(self, client):
        self._client = client


class BaseRequest(object):

    def as_payload(self):
        return self.__dict__
