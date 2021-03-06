"""
WSGI config for mailsys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailsys.settings')

application = get_wsgi_application()
sys.path.append('/usr/local/python3/lib/python3.7/site-packages')
