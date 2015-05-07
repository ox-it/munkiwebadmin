"""
WSGI config for munkiwebadmin project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import site
import sys


# Remember original sys.path.
prev_sys_path = list(sys.path)

# we add currently directory to path and change to it
pwd    = os.path.dirname(os.path.abspath(__file__))
venvwd = os.path.dirname(pwd)

sys.path = [venvwd, pwd ] + sys.path
os.chdir(venvwd)
# find the site-packages within the local virtualenv
for python_dir in os.listdir('lib'):
    site_packages_dir = os.path.join('lib', python_dir, 'site-packages')
    if os.path.exists(site_packages_dir):
        site.addsitedir(os.path.abspath(site_packages_dir))

new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "munkiwebadmin.settings"
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "munkiwebadmin.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

