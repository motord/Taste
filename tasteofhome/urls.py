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
    Rule('/data/tags', endpoint='data.tags', view='tasteofhome.data.tags'),
    Rule('/tag/<key>', endpoint='tag', view='tasteofhome.views.tag'),
  )
]

