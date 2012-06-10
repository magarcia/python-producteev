# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
from utils import unescape

LANG_ID = ('English', 'Français', 'Italiano', 'Deutsch')
SORT_BY = ('deadline', 'manager', 'labels', 'time_lastchange',
           'workspace', 'priority', 'title', 'time_created')


class User(object):
    """
    User represents an user entity in Producteev.
    """

    class __raw:
            pass

    def __init__(self, api, id=None):
        self.__api = api
        self.__get_user_info(id)

    def __get_user_info(self, id):
        if isinstance(id, int):
            values = self.__api.call('users/view', id_colleague=id)['user']
        else:
            values = self.__api.call('users/view')['user']
        self.__reload(values)

    def __cmp__(self, other):
        return self.id - other.id

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.firstname = unescape(self.__raw.firstname)
        self.lastname = unescape(self.__raw.lastname)
        self.company = unescape(self.__raw.company)
        self.colleagues = self.__raw.colleagues
        self.id = int(self.__raw.id_user)
        self.lang = LANG_ID[int(self.__raw.lang) + 1]

    def __full_name():
        def fget(self):
            return '%s %s' % (self.firstname, self.lastname)

        def fset(self, value):
            full_name = value.split(' ')
            self.firstname = full_name.pop(0)
            self.lastname = ' '.joint(full_name)

        return locals()
    full_name = property(**__full_name())

    def __default_dashboard():
        def fget(self):
            return self.__api.dashboards.get(int(self.__raw.default_dashboard))

        def fset(self, value):
            from dashboards import Dashboard

            if isinstance(value, int):
                pass
            elif isinstance(value, Dashboard):
                value = value.id
            elif isinstance(value, str):
                try:
                    value = int(value)
                except:
                    # TODO: raise error
                    value = None
            else:
                # TODO: raise error
                value = None

            if not value is None:
                user = self.__api.call('users/set_default_dashboard',
                                        id_dashboard=value)['user']
                self.__reload(user)

        return locals()
    default_dashboard = property(**__default_dashboard())

    def __sort_by():
        def fget(self):
            return SORT_BY[int(self.__raw.sort_by) - 1]

        def fset(self, value):
            if isinstance(value, int):
                value += 1
            elif isinstance(value, str):
                try:
                    value = int(value) + 1
                except:
                    try:
                        value = SORT_BY.index(value.lower()) + 1
                    except:
                        # TODO: raise error
                        value = None
            else:
                # TODO: raise error
                value = None

            if not value is None:
                user = self.__api.call('users/set_sort_by',
                                       sort=value)['user']
                self.__reload(user)

        return locals()
    sort_by = property(**__sort_by())

    def __timezone():
        def fget(self):
            return self.__raw.timezone

        def fset(self, value):
            user = self.__api.call('users/set_timezone',
                                   timezone=value)['user']
            self.__reload(user)

        return locals()
    timezone = property(**__timezone())


class Users(object):
    """
    Users give an interface for manage users in Producteev.
    """

    def __init__(self, api):
        self.__api = api
        self.me = User(self.__api)

    def __list():
        def fget(self):
            return self.me.colleagues

        def fset(self):
            pass

        return locals()
    list = property(**__list())

    def get(self, id):
        if isinstance(id, int):
            pass
        elif isinstance(id, User):
            id = id.id
        elif isinstance(id, str):
            try:
                id = int(id)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None
        return User(self.__api, id)
