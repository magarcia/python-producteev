# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.

from hashlib import md5
from urllib import urlencode
import urllib2
import json
import logging
from datetime import datetime

from users import Users
from activities import Activities
from labels import Labels
from tasks import Tasks
from dashboards import Dashboards
from subtasks import Subtasks


#: Logger for core module
LOGGER = logging.getLogger('producteev.core')

PRODUCTEEV_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S"


class ProducteevError(Exception):
    """
    """
    def __init__(self, type, message, response=None):
        self.type = type
        self.message = message
        self.response = response

    def __str__(self):
        return "%s (%s)" % (self.type, self.message)

    def __repr__(self):
        return "%s(type=%s)" % (self.__class__.__name__, self.type)


class AuthError(ProducteevError):
    def __init__(self, message, response=None):
        super(AuthError, self).__init__('Authentication Error', message, response)


class Producteev(object):
    """
    """
    BASE_URL = "https://api.producteev.com/"

    def __init__(self, api_key, secret):
        """
        """
        self.api_key = api_key
        self.secret = secret
        self.user = None
        self.token = None

    def __sign_params(self, params={}):
        """
        Add a signature hash to params.
        """
        params["api_key"] = self.api_key
        plain_signature = ''.join(
            [''.join(p) for p in sorted(params.items(), key=lambda t: t[0])])
        plain_signature += self.secret
        params["api_sig"] = md5(plain_signature).hexdigest()
        return params

    def __compose_url(self, path, params=None):
        """
        Compose url from path and params.
        """
        params = self.__sign_params(params)
        return "%s%s?%s" % (self.BASE_URL, path, urlencode(params))

    def __handle_response(self, response):
        """
        Load response to python dictonary.
        """
        return json.loads(response.read())

    def __request(self, path, **params):
        for k, v in params.items():
            params[k] = str(v)
        url = self.__compose_url(path, params)
        r = urllib2.urlopen(url)
        return self.__handle_response(r)

    def call(self, path, **params):
        if not self.token:
            raise AuthError('Token undefined, login required')
        return self.__request(path, token=self.token, **params)

    def get_time(self):
        """
        Get time from Producteev server.
        """
        time = self.call('time.json')['time']['value']
        LOGGER.debug(time)
        return datetime.strptime(
            ' '.join(time.split(' ')[0:-1]),
            PRODUCTEEV_DATE_FORMAT)

    def login(self, email, password):
        """
        Login user to API.
        """
        response = self.__request(
                        'users/login.json',
                        email=email,
                        password=password)
        self.token = response['login']['token']
        self.users = Users(self)
        self.tasks = Tasks(self)
        self.dashboards = Dashboards(self)
        self.labels = Labels(self)
        self.activities = Activities(self)
        self.subtasks = Subtasks(self)
        LOGGER.debug('Loged')
