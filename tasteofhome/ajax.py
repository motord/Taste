# -*- coding: utf-8 -*-
# __author__ = 'peter'

from kay.utils import render_json_response
from yan.auth.decorators import login_required
from decorators import with_tag
import simplejson
from models import Tag

class TagEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tag):
            return {"key": obj.key().__str__(), "name":obj.name}
        return simplejson.JSONEncoder.default(self, obj)

@login_required
@with_tag
def markmap(request, tag):
    if request.method == 'POST':
        user=request.user
        user.add_tag(tag)
        return render_json_response(tag, simplejson_kwargs={"cls":TagEncoder})





