try:
    from envy.wsgi import WSGI
    from urls import urls
    from envy.session import CookieSession
    import logging
    import settings

    logging.basicConfig(format=settings.LOG_FORMAT, level=settings.LOG_LEVEL)

    server_settings = dict(
        template_dirs=settings.TEMPLATE_DIRS, 
        session_key='automaton_session', 
        session_cls=CookieSession
    )    
except Exception as e:
    print e

wsgi = WSGI(urls, server_settings)

def log_request(self):
    log = self.server.log
    if log:
        if hasattr(log, "info"):
            log.info(self.format_request())
        else:
            log.write(self.format_request())

import gevent
gevent.pywsgi.WSGIHandler.log_request = log_request

def serve(env, start_response):
    try:        
        return wsgi.serve(env, start_response)
    except Exception as e:
        print e
