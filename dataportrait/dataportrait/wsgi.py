"""
WSGI config for dataportrait project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

# sys.path.append('/home/development/projects/dataprtrait/dataportrait')
#
# sys.path.appen('/home/development/.virtualenvs/dataportrait/lib/python3.5/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataportrait.settings")

application = get_wsgi_application()
