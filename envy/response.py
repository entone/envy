import Cookie

class Response(object):
    body = ""
    headers = None
    status = '200 OK'
    _cookie = None
    
    def __init__(self, body, status='200 OK', headers=None):
        self.body = body
        self.status = status
        self._cookie = Cookie.SimpleCookie()
        self.headers = headers if headers else [('Content-type', 'text/html')]
        self.headers.append(('Content-Length', str(len(self.body))))


    def cookie(self, key, value, expires='', path='/', httponly=False):
        self._cookie[key] = value
        self._cookie[key]['expires'] = expires
        self._cookie[key]['path'] = path
        self._cookie[key]['httponly'] = httponly
        self.headers.append(('set-cookie', self._cookie[key].output(header='')))


