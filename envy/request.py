import urlparse
import Cookie

class Request(object):
    env = None
    GET = {}
    def __init__(self, env):
        self.env = env
        self.GET = urlparse.parse_qs(env['QUERY_STRING'])
        self.COOKIE = Cookie.SimpleCookie(env['HTTP_COOKIE'])