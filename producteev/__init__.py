"Producteev API library for Python."
# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.

import __version
from .core import Producteev, AuthError
from .timezones import Zones as TimeZones

VERSION = __version.tuple

__author__ = "Martin Garcia"
__contact__ = "newluxfero@gmail.com"
__homepage__ = "http://github.com/magarcia/python-producteev"
__version__ = __version.dotted
