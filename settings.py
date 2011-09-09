# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'ReplaceItWithSecretString'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
)

TEMPLATE_DIRS = (
)

USE_I18N = False
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
    'yan.auth',
    'tasteofhome',
)

APP_MOUNT_POINTS = {
    'tasteofhome':'/',
}

# You can remove following settings if unnecessary.
CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'yan.context_processors.url_functions',
  'kay.context_processors.media_url',
  'yan.auth.context_processors.login_box',
)

JINJA2_FILTERS = {
#    'date': 'django.template.defaultfilters.date',
#    'time': 'django.template.defaultfilters.time',
#    'timesince': 'django.template.defaultfilters.timesince',
#    'timeuntil': 'django.template.defaultfilters.timeuntil',
    'smartdatetime': 'yan.utils.filters.smartdatetime',
    'nl2br': 'kay.utils.filters.nl2br',
}

MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'yan.auth.middleware.AuthenticationMiddleware',
    'kay.ext.appstats.middleware.AppStatsMiddleware',
)
REVERSE_PROXIED_DOMAIN='jxw.samdeha.com'
AUTH_USER_BACKEND='yan.auth.backends.datastore.DatastoreBackendWithReverseProxiedDomainHack'
AUTH_USER_MODEL = 'tasteofhome.models.User'

ITEMS_PER_PAGE = 20

RECAPTCHA_PUBLIC_KEY='6LdmQ8cSAAAAAFHs5pU2GjGLBRDV0S8Uhe3m9zF7 '
RECAPTCHA_PRIVATE_KEY='6LdmQ8cSAAAAAMlyVpCA5TjdYzmf_GMxl6fAXtY2'