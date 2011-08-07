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

# Create your views here.

def index(request):
  return render_to_response('tasteofhome/index.html', {'message': 'Hello'})

def forum(request):
  return render_to_response('tasteofhome/forum.html')

def populate(request):
    for t in [u'北京市',u'天津市',u'河北省',u'山西省',u'内蒙古自治区',u'辽宁省',u'吉林省',u'黑龙江省',u'上海市',u'江苏省',u'浙江省',u'安徽省',u'福建省',u'江西省',u'山东省',u'河南省',u'湖北省',u'湖南省',u'广东省',u'海南省',u'广西壮族自治区',u'甘肃省',u'陕西省',u'新 疆维吾尔自治区',u'青海省',u'宁夏回族自治区',u'重庆市',u'四川省',u'贵州省',u'云南省',u'西藏自治区',u'台湾省',u'澳门特别行政区',u'香港特别行政区']:
        tag=Tag(name=t)
        tag.put()
    return  render_to_response('tasteofhome/index.html', {'message': 'province'})