from .response import Response
from .session import Session
from .session import SessionEnd
from .request import Request
from mako.lookup import TemplateLookup
import logging
import json

class WSGI(object):
    urls = None
    settings = None

    def __init__(self, urls, settings=None):
        self.urls = urls
        self.settings = settings
        self.settings['templates'] = TemplateLookup(directories=self.settings.get('template_dirs'), output_encoding='utf-8', encoding_errors='replace')

    def match(self, path):
        for u in self.urls:
            res = u.match(path)
            if res: return u
        return False

    def serve(self, env, start_response, session=None):
        try:
            url = self.match(env['PATH_INFO'][1:])
            request = Request(env)
            session_key = request.COOKIE.get(self.settings.get('session_key'))
            try:
                session = self.settings.get("session_cls")(key=session_key, request=request)
            except SessionEnd as e:
                if env.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    res = Response(body=json.dumps(dict(status='redirect', location=self.settings.get('session_end_redirect'))))
                else:
                    res = Response(body='SessionEnded', status='301 Moved Permanently', headers=[('Location', self.settings.get('session_end_redirect'))])
                res.cookie(self.settings.get('session_key'), "")
                start_response(res.status, res.headers)
                return res.body
            except Exception as e:
                session = self.settings.get("session_cls")(key=None, request=request)
        except Exception as e:
            logging.exception(e)
        if url:
            try:
                controller = url.cls(request=request, session=session, settings=self.settings)
                response = getattr(controller, url.meth)(**url.kwargs)
                controller.session.save(response=response)
            except Exception as e:
                logging.exception(e)
                response = Response(e.message, status='500 Internal Server Error')
        else:
            response = Response("404 Not Found: %s" % env['PATH_INFO'][1:], status='404 Not Found')
        

        if response:
            start_response(response.status, response.headers)
            return response.body