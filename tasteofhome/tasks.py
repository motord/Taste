# -*- coding: utf-8 -*-
# __author__ = 'peter'

from kay.utils.decorators import cron_only
from mapreduce.control import start_map

import kay
kay.setup()

@cron_only
def update_view_count(request):
    start_map(name='Update view count',
              handler_spec='tasteofhome.mapper.update_view_count',
              reader_spec='mapreduce.input_readers.DatastoreInputReader',
              mapper_parameters={'entity_kind': 'tasteofhome.models.Course'})