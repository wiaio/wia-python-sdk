import sys

class WiaError(object):
    def __new__(cls, *p, **k):
        inst = object.__new__(cls)
        return inst

    def __init__(self, response):
        self.status_code = response.status_code
        self.json = response.json()
        self.headers = response.headers
        #self.message = message

# Status code: 400
class WiaValidationError(WiaError):
    pass

# Status code: 401
class WiaUnauthorisedError(WiaError):
    pass

# Status code: 403
class WiaForbiddenError(WiaError):
    pass

# Status code: 404
class WiaNotFoundError(WiaError):
    pass
