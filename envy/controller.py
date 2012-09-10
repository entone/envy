from mako import exceptions
import logging
from logging.handlers import SysLogHandler

class Controller(object):
    request = None
    session = None
    settings = None

    def __init__(self, request=None, session=None, settings=None):
        self.request = request
        self.session = session
        self.settings = settings
        self.logger = logging.getLogger("%s.%s" % (self.__module__, self.__class__.__name__))
        handler = SysLogHandler(address='/dev/log')
        self.logger.addHandler(handler)

    def render(self, temp, **kwargs):
        try:
            t = self.settings.get('templates').get_template(temp)
            return t.render(**kwargs)
        except:
            return exceptions.html_error_template().render()