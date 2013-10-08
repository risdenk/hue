#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Misc helper functions
"""

try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

import logging
import re
import time
from time import strftime

LOG = logging.getLogger(__name__)
_NAME_REGEX = re.compile('^[a-zA-Z][\-_a-zA-Z0-0]*$')


def parse_timestamp(timestamp, time_format=None):
  """
  parse_timestamp(timestamp, time_format=None) -> struct_time

  Does NOT raise ValueError. Return None on formatting error.
  """
  if time_format is None:
    time_format = '%a, %d %b %Y %H:%M:%S %Z'
  try:
    return time.strptime(timestamp, time_format)
  except ValueError:
    LOG.error("Failed to convert Oozie timestamp: %s" % (time_format,), exc_info=1)
    return None


def config_gen(dic):
  """
  config_gen(dic) -> xml for Oozie workflow configuration
  """
  sio = StringIO()
  print >> sio, '<?xml version="1.0" encoding="UTF-8"?>'
  print >> sio, "<configuration>"
  for k, v in dic.iteritems():
    print >> sio, "<property>\n  <name>%s</name>\n  <value><![CDATA[%s]]></value>\n</property>\n" \
        % (k, v)
  print >>sio, "</configuration>"
  sio.flush()
  sio.seek(0)
  return sio.read()


def is_valid_node_name(name):
  return _NAME_REGEX.match(name) is not None

def format_time(time, format='%d %b %Y %H:%M:%S'):
  if time is None:
    return ''

  if type(time) == unicode:
    return time
  else:
    return strftime(format, time)
