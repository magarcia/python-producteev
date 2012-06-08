# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.

# TODO:
# activities/show_activities
# activities/show_notifications
# activities/notifications_set_read
# activities/set_read


class Activity(object):

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_activity

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_activity

    def mark_read(self):
        return 'Not implemented yet'


class Activities(object):
    def __init__(self, api):
        self.__api = api

    def __list():
        def fget(self):
            return 'Not implemented yet'

        def fset(self):
            pass

        return locals()
    list = property(**__list())

    def __notifications():
        def fget(self):
            return 'Not implemented yet'

        def fset(self):
            pass

        return locals()
    notifications = property(**__notifications())

    def set_read(self, since):
        return 'Not implemented yet'
