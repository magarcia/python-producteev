# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
from utils import unescape
import logging
import re

LOGGER = logging.getLogger('producteev.dashboards')

# TODO:
# dashboards/confirm
# dashboards/refuse
# dashboards/need_upgrade_list
# dashboards/needs_upgrade
# dashboards/reorder


class Dashboard(object):

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_dashboard

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_dashboard

    def __str__(self):
        return self.title

    def __title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            dashboard = self.__api.call('dashboards/set_title.json',
                                        id_dashboard=self.id,
                                        title=value)['dashboard']
            self.__reload(dashboard)

        return locals()
    title = property(**__title())

    def __access():
        def fget(self):
            from users import User
            users = self.__api.call('dashboards/access.json',
                                    id_dashboard=self.id)['accesslist']
            return [User(self.__api, x['user']) for x in users]

        def fset(self):
            pass

        return locals()
    users = property(**__access())

    def __tasks():
        def fget(self):
            from tasks import Task
            tasks = self.__api.call('dashboards/tasks.json',
                                    id_dashboard=self.id)['tasks']
            return [Task(self.__api, x['task']) for x in tasks]

        def fset(self):
            pass

        return locals()
    tasks = property(**__tasks())

    def leave(self):
        return self.__api.call('dashboards/leave.json', id_dashboard=self.id)

    def enable_smart_labels(self):
        dashboard = self.__api.call('dashboards/leave.json',
                                    id_dashboard=self.id, on=1)['dashboard']
        return Dashboard(self.__api, dashboard)

    def disable_smart_labels(self):
        dashboard = self.__api.call('dashboards/leave.json',
                                    id_dashboard=self.id, on=0)['dashboard']
        return Dashboard(self.__api, dashboard)

    def smart_labels(self, value):
        if value is True:
            self.enable_smart_labels()
        else:
            self.disable_smart_labels()

    def delete(self):
        return self.__api.call('dashboards/delete.json', id_dashboard=self.id)

    def invite(self, value, message=None):
        from users import User
        kwargs = {}
        if isinstance(value, User):
            kwargs['id_user_to'] = value
            if message:
                kwargs['message'] = message
            dashboard = self.__api.call('dashboards/invite_user_by_id.json',
                                        **kwargs)['dashboard']
        elif isinstance(value, int):
            kwargs['id_user_to'] = value
            if message:
                kwargs['message'] = message
            dashboard = self.__api.call('dashboards/invite_user_by_id.json',
                                        **kwargs)['dashboard']
        elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", value) != None:
            kwargs['email'] = value
            if message:
                kwargs['message'] = message
            dashboard = self.__api.call('dashboards/invite_user_by_id.json',
                                        **kwargs)['dashboard']
        return Dashboard(self.__api, dashboard)


class Dashboards(object):

    def __init__(self, api):
        self.__api = api

    def new(self, title):
        return Dashboard(self.__api, self.__api.call('dashboards/create.json',
                                title=title)['dashboard'])

    def get(self, value):
        if isinstance(value, int):
            dashboard = Dashboard(self.__api,
                                self.__api.call('dashboards/view.json',
                                id_dashboard=value)['dashboard'])
        elif isinstance(value, Dashboard):
            dashboard = Dashboard(self.__api,
                                self.__api.call('dashboards/view.json',
                                id_dashboard=value.id)['dashboard'])
        else:
            dashboard = None
        return dashboard

    def __list():
        def fget(self):
            dashboards = self.__api.call('dashboards/show_list.json')['dashboards']
            return [Dashboard(self.__api, x['dashboard']) for x in dashboards]

        def fset(self):
            pass

        return locals()
    list = property(**__list())
