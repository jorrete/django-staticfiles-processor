from os.path import join

from django.conf import settings


TMP_DIR = getattr(settings, 'TMP_DIR', '/tmp')

STATICFILES_BUILD = getattr(settings, 'STATICFILES_BUILD', join(TMP_DIR, 'staticfiles_build'))

STATICFILES_PROCESSORS = getattr(settings, 'STATICFILES_PROCESSORS', [])

STATICFILES_PROCESSORS_CACHE = getattr(settings, 'STATICFILES_PROCESSORS_CACHE', False)
