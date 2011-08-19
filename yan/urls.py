# -*- coding: utf-8 -*-
# yan.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('yan/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'yan/index': 'yan.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='yan.views.index'),
  )
]

