import re
from .request import Request

class URL(object):
    pattern = None
    method = None
    compiled = None
    kwargs = None
    
    def __init__(self, pattern, method):
        self.pattern = pattern
        self.method = method
        self.compiled = re.compile(self.pattern)

    def match(self, path):
        res = self.compiled.match(path)
        if res:
            self.kwargs = res.groupdict()
            return True
        return False

    def cls(self, env, settings):
        return self.method.im_class(Request(env), settings)

    @property
    def meth(self):
        return self.method.__name__