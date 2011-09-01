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
from decorators import with_tag, with_course, update_view_count, admin_or_owner_required
from kay.utils.paginator import Paginator
from google.appengine.api import memcache

# Create your views here.

def index(request):
  tags=memcache.get('tags::1')
  if tags is None:
      tags=Tag.gql("WHERE depth = :1", 1)
      memcache.set('tags::1', tags)
  return render_to_response('tasteofhome/index.html', {'tags': tags})

def tag(request, key):
  tag=memcache.get(key)
  if tag is None:
      tag=db.get(key)
      memcache.set(key, tag)
  tags=memcache.get(key+'::tags')
  if tags is None:
      tags=Tag.gql("WHERE ANCESTOR IS :1 AND depth = :2", tag, tag.depth+1)
      memcache.set(key+'::tags', tags)
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
@admin_or_owner_required
def edit_course(request, course):
  form=CourseForm(instance=course, initial={'owner': course.owner})
  if request.method == 'POST':
      if form.validate(request.form):
          form.save(owner=user, crud=CRUD.Update)
          return
  return render_to_response('tasteofhome/edit_course.html', {'tag': tag, 'form': form})


@cache_page(60)
def forum_discussions(request):
  return forum_discussions_page(request, 1)

def forum_categories():
    categories=memcache.get('forum::categories')
    if categories is None:
        categories=Tag.gql("WHERE depth = :1", 100)
        memcache.set('forum::categories', categories)
    return categories

def forum_discussions_page(request, page):
  discussions=Course.all()
  p=Paginator(discussions, settings.ITEMS_PER_PAGE)
  return render_to_response('tasteofhome/discussions.html', {'discussions': discussions, 'categories': forum_categories(), 'paginator': p})

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
@admin_or_owner_required
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
    return render_to_response('tasteofhome/discussion.html', {'discussion': discussion, 'form':form, 'categories': forum_categories()})

@with_tag
def forum_category(request, tag):
    return forum_category_page(request, tag, 1)

def forum_category_page(request, tag, page):
  discussions=Course.gql("WHERE ANCESTOR IS :1", tag)
  tags=Tag.gql("WHERE depth = :1", 100)
  return render_to_response('tasteofhome/forum_category.html', {'discussions': discussions, 'category':tag, 'categories': forum_categories()})


def user(request, user_name):
    user=User.gql("WHERE user_name = :1", user_name).get()
    return render_to_response('tasteofhome/user.html', {'user': user})



def termsofservice(request):
  return render_to_response('tasteofhome/termsofservice.html')

def robots(request):
    return render_to_response('tasteofhome/robots.txt')