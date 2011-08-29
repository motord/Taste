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
from models import Tag, Course, Message, User, CourseMessagesIndex
from forms import CourseForm, DiscussionForm, MessageForm
from google.appengine.ext import db
from lib import recaptcha
from kay.conf import settings
from kay.cache.decorators import no_cache, cache_page
from yan.auth.decorators import login_required
from werkzeug import redirect
from forms import CRUD
from decorators import with_tag, with_course, update_view_count

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

@with_course
@update_view_count(1)
def course(request, course):
  return render_to_response('tasteofhome/course.html', {'course': course})

@login_required
@with_tag
def new_course(request, tag):
  form=CourseForm(initial={'tag':tag, 'owner':request.user})
  if request.method == 'POST':
      if form.validate(request.form):
          form.save(owner=user, crud=CRUD.Create)
          return redirect('')
  return render_to_response('tasteofhome/new_course.html', {'form': form.as_widget()})

@login_required
@with_course
def edit_course(request, course):
  form=CourseForm(instance=course, initial={'owner': course.owner})
  if request.method == 'POST':
      if form.validate(request.form):
          form.save(owner=user, crud=CRUD.Update)
          return
  return render_to_response('tasteofhome/edit_course.html', {'tag': tag, 'form': form})


@cache_page(60)
def forum_discussions(request):
  discussions=Course.all()
  tags=Tag.gql("WHERE depth = :1", 100)
  return render_to_response('tasteofhome/discussions.html', {'discussions': discussions, 'tags': tags})

@login_required
def new_discussion(request):
  form=DiscussionForm(initial={'owner':request.user})
  if request.method == 'POST':
      if form.validate(request.form):
          form.save(crud=CRUD.Create)
          return redirect(url_for('tasteofhome/forum.discussions'))
  return render_to_response('tasteofhome/new_discussion.html', {'form': form.as_widget()})

@login_required
@with_course
def edit_discussion(request, course):
  form=DiscussionForm(instance=course, initial={'owner': course.owner})
  if request.method == 'POST':
      if form.validate(request.form):
          form.save(owner=user, crud=CRUD.Update)
          return
  return render_to_response('tasteofhome/edit_discussion.html', {'form': form.as_widget()})

@with_course
@update_view_count(1)
def forum_discussion(request, course):
    discussion=course
    tags=Tag.gql("WHERE depth = :1", 100)
    form=MessageForm()
    return render_to_response('tasteofhome/discussion.html', {'discussion': discussion, 'form':form, 'tags': tags})

@with_tag
def forum_category(request, tag):
  discussions=Course.gql("WHERE ANCESTOR IS :1", tag)
  return render_to_response('tasteofhome/discussions.html', {'discussions': discussions})

def user(request, user_name):
    user=User.gql("WHERE user_name = :1", user_name).get()
    return render_to_response('tasteofhome/user.html', {'user': user})



def termsofservice(request):
  return render_to_response('tasteofhome/termsofservice.html')

def robots(request):
    return render_to_response('tasteofhome/robots.txt')