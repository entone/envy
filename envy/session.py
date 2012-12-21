class SessionEnd(Exception):pass

class Session(dict):
    key = None
    request = None

    def __init__(self, key=None, request=None):
        dict.__init__(self)
        self.key = key
        self.request = request

    def __setattr__(self, key, val):
        if key in ['key', 'request']: self.__dict__[key] = val
        else: self[key] = val

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            return None

    def save(self): pass


class CookieSession(Session):

    def __init__(self, key=None, request=None):
        super(CookieSession, self).__init__(key=key, request=request)
        for k,v in self.request.COOKIE.iteritems(): setattr(self, k, v.value)

    def save(self, response):
        for k,v in self.iteritems(): response.cookie(k, v)



