# -*- coding: utf-8 -*-

"""
Kay cache decorators

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from werkzeug.exceptions import NotFound

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
            course.update_view_count(n)
            return fun(request, course)
        return wrapped
    return decorate

