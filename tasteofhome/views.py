# -*- coding: utf-8 -*-
"""
tasteofhome.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""

from kay.utils import render_to_response, url_for
from models import Tag, Course, Message, User
from forms import CourseForm, DiscussionForm, MessageForm
from google.appengine.ext import db
from lib import recaptcha
from kay.conf import settings
from yan.auth.decorators import login_required
from werkzeug import redirect
from werkzeug.exceptions import NotFound

# Create your views here.

def index(request):
  tags=Tag.gql("WHERE depth = :1", 1)
  return render_to_response('tasteofhome/index.html', {'tags': tags})

def tag(request, key):
  tag=db.get(key)
  tags=Tag.gql("WHERE ANCESTOR IS :1 AND depth = :2", tag, tag.depth+1)
  return render_to_response('tasteofhome/tag.html', {'tag': tag, 'tags': tags})

def register(request):
  return render_to_response('tasteofhome/register.html', {'captcha': recaptcha.displayhtml(public_key = settings.RECAPTCHA_PUBLIC_KEY,
                                                                                           use_ssl = False,
                                                                                           error = None)})

def course(request, key):
  course=db.get(key)
  return render_to_response('tasteofhome/course.html', {'course': course})

def with_course(fun):
    def decorate(self, course_key=None):
        course=None
        if course_key:
            course=db.get(course_key)
            if not course:
                raise NotFound
        return fun(self, course)
    return decorate

def with_tag(fun):
    def decorate(self, tag_key=None):
        tag=None
        if tag_key:
            tag=db.get(tag_key)
            if not tag:
                raise NotFound
        return fun(self, tag)
    return decorate

@login_required
@with_tag
def new_course(request, tag):
  form=CourseForm(initial={'tag':tag, 'owner':request.user})
  if request.method == 'POST':
      if form.validate(request.form):
          return redirect('')
  return render_to_response('tasteofhome/new_course.html', {'form': form.as_widget()})

@login_required
@with_course
def edit_course(request, course):
  form=CourseForm(instance=course)
  if request.method == 'POST':
      if form.validate(request.form):
          if request.user.is_authenticated():
              user=request.user
          else:
              user=None
          new_course=form.save(owner=user)
          return
  return render_to_response('tasteofhome/edit_course.html', {'tag': tag})



def forum(request):
  discussions=Course.all()
  return render_to_response('tasteofhome/forum.html', {'discussions': discussions})

@login_required
def new_discussion(request):
  form=DiscussionForm(initial={'owner':request.user})
  if request.method == 'POST':
      if form.validate(request.form):
          form.save(create=True)
          return redirect(url_for('tasteofhome/forum'))
  return render_to_response('tasteofhome/new_discussion.html', {'form': form.as_widget()})

@login_required
@with_course
def edit_discussion(request, course):
  form=DiscussionForm(instance=course)
  if request.method == 'POST':
      if form.validate(request.form):
          new_course=form.save(owner=user)
          return
  return render_to_response('tasteofhome/edit_discussion.html', {'tag': tag})

@with_course
def forum_discussion(request, course):
    discussion=course
    form=MessageForm()
    return render_to_response('tasteofhome/discussion.html', {'discussion': discussion})

@with_tag
def forum_category(request, tag):
  discussions=Course.gql("WHERE ANCESTOR IS :1", tag)
  return render_to_response('tasteofhome/forum.html', {'discussions': discussions})

def user(request, user_name):
    user=User.gql("WHERE user_name = :1", user_name).get()
    return render_to_response('tasteofhome/user.html', {'user': user})



def termsofservice(request):
  return render_to_response('tasteofhome/termsofservice.html')

def robots(request):
    return render_to_response('tasteofhome/robots.txt')