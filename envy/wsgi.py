from .response import Response
from .session import Session
from .request import Request
from mako.lookup import TemplateLookup
import logging

class WSGI(object):
    urls = None
    settings = None

    def __init__(self, urls, settings=None):
        self.urls = urls
        self.settings = settings
        self.settings['templates'] = TemplateLookup(directories=self.settings.template_dirs, output_encoding='utf-8', encoding_errors='replace')

    def match(self, path):
        for u in self.urls:
            res = u.match(path)
            if res: return u
        return False

    def serve(self, env, start_response):
        url = self.match(env['PATH_INFO'][1:])        
        request = Request(env)
        session_key = request.COOKIES.get(self.settings.get('session_key'))
        session = self.settings.get("session_cls")(key=session_key, request=request)
        if url:
            try:
                controller = url.cls(request, session, self.settings)
                response = getattr(controller, url.meth)(**url.kwargs)
                controller.session.save(response=response)
            except Exception as e:
                logging.exception(e)
                response = Response(e.message, status='500 Internal Server Error')
        else:
            response = Response("404 Not Found: %s" % env['PATH_INFO'][1:], status='404 Not Found')
        
        start_response(response.status, response.headers)
        return response.body