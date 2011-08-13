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

from kay.utils import render_to_response
from models import Tag
from google.appengine.ext import db

# Create your views here.

def index(request):
  tags=Tag.gql("WHERE depth = :1", 1)
  return render_to_response('tasteofhome/index.html', {'tags': tags})

def tag(request, key):
  tag=db.get(key)
  tags=Tag.gql("WHERE ANCESTOR IS :1 AND depth = :2", tag, tag.depth+1)
  return render_to_response('tasteofhome/tag.html', {'tag': tag, 'tags': tags})

def forum(request):
  tags=Tag.gql("WHERE depth = :1", 100)
  return render_to_response('tasteofhome/forum.html', {'tags': tags})
