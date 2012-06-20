from envy.url import URL
from controllers.test import Test

urls = (
    URL(r'^help/(?P<category>[-\w]+)/?$', Test.woot),
)