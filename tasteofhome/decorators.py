# -*- coding: utf-8 -*-

"""
Kay cache decorators

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from werkzeug.exceptions import NotFound, Forbidden
from functools import update_wrapper
from werkzeug import redirect

from kay.utils.decorators import auto_adapt_to_methods
from kay.utils import local

def with_course(fun):
    def decorate(request, course_key=None):
        course=None
        if course_key:
            course=db.get(course_key)
            if not course:
                raise NotFound
        return fun(request, course)
    return decorate

def with_tag(fun):
    def decorate(request, tag_key=None):
        tag=None
        if tag_key:
            tag=db.get(tag_key)
            if not tag:
                raise NotFound
        return fun(request, tag)
    return decorate

def update_view_count(n):
    def decorate(fun):
        def wrapped(request, course):
            course.update_view_count_memcache(n)
            return fun(request, course)
        return wrapped
    return decorate

def admin_or_owner_required(func):
  def inner(request, course, *args, **kwargs):
    if not request.user.is_admin:
      if not request.user!=course.owner:
          if request.user.is_anonymous():
            return redirect(local.app.auth_backend.create_login_url(request.url))
          else:
            # TODO: Lead to more user friendly error page.
            raise Forbidden(
              description =
              '<p>You don\'t have the permission to access the requested resource.'
              ' It is either read-protected or not readable by the server.</p>'
              ' Maybe you want <a href="%s">logout</a>?' %
              local.app.auth_backend.create_logout_url(request.url)
            )
    return func(request, course, *args, **kwargs)
  update_wrapper(inner, func)
  return inner

admin_or_owner_required = auto_adapt_to_methods(admin_or_owner_required)