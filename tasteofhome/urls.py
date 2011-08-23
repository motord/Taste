# -*- coding: utf-8 -*-
# tasteofhome.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('tasteofhome/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'tasteofhome/index': 'tasteofhome.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='tasteofhome.views.index'),
    Rule('/forum', endpoint='forum', view='tasteofhome.views.forum'),
    Rule('/register', endpoint='register', view='tasteofhome.views.register'),
    #Rule('/data/tags', endpoint='data.tags', view='tasteofhome.data.tags'),
    #Rule('/data/forum', endpoint='data.forum', view='tasteofhome.data.forum'),
    #Rule('/data/create_admin', endpoint='data.create_admin', view='tasteofhome.data.create_admin'),
    Rule('/tag/<key>', endpoint='tag', view='tasteofhome.views.tag'),
    Rule('/course/<key>', endpoint='course', view='tasteofhome.views.course'),
    Rule('/new/course/<tag_key>', endpoint='new.course', view='tasteofhome.views.new_course'),
    Rule('/edit/course/<course_key>', endpoint='edit.course', view='tasteofhome.views.edit_course'),
    Rule('/new/discussion', endpoint='new.discussion', view='tasteofhome.views.new_discussion'),
    Rule('/edit/discussion/<course_key>', endpoint='edit.discussion', view='tasteofhome.views.edit_discussion'),
    Rule('/termsofservice', endpoint='termsofservice', view='tasteofhome.views.termsofservice'),
    Rule('/robots.txt', endpoint='robots', view='tasteofhome.views.robots'),
  )
]

