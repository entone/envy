from .response import Response
from mako.lookup import TemplateLookup
import time
import logging

class WSGI(object):
    urls = None
    settings = None

    def __init__(self, urls, settings=None):
        self.urls = urls
        self.settings = settings
        self.settings['templates'] = TemplateLookup(directories=self.settings.get("template_dirs"), output_encoding='utf-8', encoding_errors='replace')

    def match(self, path):
        for u in self.urls:
            res = u.match(path)
            if res: return u
        return False

    def serve(self, env, start_response):
        start = time.time()
        url = self.match(env['PATH_INFO'][1:])
        data = None
        if url:
            try:
                response = getattr(url.cls(env, self.settings), url.meth)(**url.kwargs)
            except Exception as e:
                logging.exception(e)
                response = Response(e.message, status='500 Internal Server Error')
        else:
            response = Response("404 Not Found: %s" % env['PATH_INFO'][1:], status='404 Not Found')
        
        total = time.time()-start
        response.headers.append(("Pageload", str(total)))
        start_response(response.status, response.headers)
        return response.body