from envy.controller import Controller
from envy.response import Response

class Test(Controller):

    def woot(self, category):
        self.logger.debug("COOKIE: %s" % self.session.woot)
        resp = Response(self.render('test.html', category=category, get=self.request.GET))
        self.session.woot = category
        self.session.holla_back = "yeaheyah"
        return resp