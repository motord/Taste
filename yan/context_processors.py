# -*- coding: utf-8 -*-

"""
Kay context processors.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.conf import settings
from kay.utils import local

def url_functions(request):
  ret = {'url_for': url_for,
         'reverse': reverse,
         'create_login_url': create_login_url,
         'create_logout_url': create_logout_url}
  if settings.USE_I18N:
    from kay.i18n import create_lang_url
    ret.update({'create_lang_url': create_lang_url})
  return ret

def url_for(endpoint, **args):
  """Get the URL to an endpoint. There are some special keyword
  arguments:

  `_anchor`
    This string is used as URL anchor.

  `_external`
    If set to `True` the URL will be generated with the full server name
    and `http://` prefix.
  """
  anchor = args.pop('_anchor', None)
  external = args.pop('_external', False)
  rv = local.url_adapter.build(endpoint, args,
                               force_external=external)
  if anchor is not None:
    from werkzeug.urls import url_quote
    rv += '#' + url_quote(anchor)
  return rv

def create_auth_url(url, action, **kwargs):
  if url is None:
    url = local.request.url
  method_name = 'create_%s_url' % action
  if 'yan.auth.middleware.GoogleAuthenticationMiddleware' in \
        settings.MIDDLEWARE_CLASSES:
    from google.appengine.api import users
    method = getattr(users, method_name)
  elif 'yan.auth.middleware.AuthenticationMiddleware' in \
        settings.MIDDLEWARE_CLASSES:
    method = getattr(local.app.auth_backend, method_name)
  return method(url, **kwargs)


def create_logout_url(url=None, **kwargs):
  """
  Get the URL for a logout page.
  """
  return create_auth_url(url, 'logout', **kwargs)


def create_login_url(url=None, **kwargs):
  """
  Get the URL for a login page.
  """
  return create_auth_url(url, 'login', **kwargs)


def reverse(endpoint, _external=False, method='GET', **values):
  """
  An utility function for jinja2.
  """
  return local.url_adapter.build(endpoint, values, method=method,
      force_external=_external)

