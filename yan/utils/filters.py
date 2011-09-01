# -*- coding: utf-8 -*-

"""
Kay utilities.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import re
from jinja2 import (
  environmentfilter, Markup, escape,
)

def smartdatetime(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
