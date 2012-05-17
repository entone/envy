# setup.py ---
#

from distutils.core import setup
from setuptools import find_packages

setup(name='Envy',
      version='0.0.1',
      author='Christopher Coté',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['gevent', 'gunicorn', 'gevent-websocket', 'mako'],
      include_package_data=True,
)

#
# setup.py ends here
