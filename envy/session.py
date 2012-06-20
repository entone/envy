class Session(dict):
    key = None
    request = None

    def __init__(self, key, request=None):
        self.key = key
        self.request = request

    def __getattr__(self, key):
        try:
            return self[key]
        except Exception as e:
            raise ValueError("%s is an invalid attribute" % key)

    def __setattr__(self, key, val):
        self[key] = val

    def save(self): pass


class CookieSession(Session):

    def __init__(self, key, request=None):
        super(CookieSession, self).__init__(key, request=request)
        for k,v in self.request.COOKIES.iteritems(): setattr(self, k, v.value)

    def save(self, response):
        for k,v in self.iteritems(): response.cookie(k, v)



