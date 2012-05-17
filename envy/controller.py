from mako import exceptions
import logging

class Controller(object):
    request = None
    settings = None

    def __init__(self, request, settings=None):
        self.request = request
        self.settings = settings
        self.logger = logging.getLogger("%s.%s" % (self.__module__, self.__class__.__name__))

    def render(self, temp, **kwargs):
        try:
            t = self.settings.get('templates').get_template(temp)
            return t.render(**kwargs)
        except:
            return exceptions.html_error_template().render()