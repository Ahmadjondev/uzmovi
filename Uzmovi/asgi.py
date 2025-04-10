"""
ASGI config for uzmovi project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Uzmovi.settings')

application = get_asgi_application()
