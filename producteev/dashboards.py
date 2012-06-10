# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
from utils import unescape
import re


class Dashboard(object):
    """
    Dashboard represents an dashboard entity in Producteev.
    """

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__reload(values)

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = int(self.__raw.id_dashboard)

    def __str__(self):
        return self.title

    def __cmp__(self, other):
        return self.id - other.id

    def __title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            dashboard = self.__api.call('dashboards/set_title',
                                        id_dashboard=self.id,
                                        title=value)['dashboard']
            self.__reload(dashboard)

        return locals()
    title = property(**__title())

    def __access():
        def fget(self):
            from users import User
            users = self.__api.call('dashboards/access',
                                    id_dashboard=self.id)['accesslist']
            return [User(self.__api, x['user']) for x in users]

        def fset(self):
            pass

        return locals()
    users = property(**__access())

    def __tasks():
        def fget(self):
            from tasks import Task
            tasks = self.__api.call('dashboards/tasks',
                                    id_dashboard=self.id)['tasks']
            return [Task(self.__api, x['task']) for x in tasks]

        def fset(self):
            pass

        return locals()
    tasks = property(**__tasks())

    def leave(self):
        resp = self.__api.call('dashboards/leave',
                                id_dashboard=self.id)['stats']['result']
        return resp == 'TRUE'

    def enable_smart_labels(self):
        dashboard = self.__api.call('dashboards/leave',
                                    id_dashboard=self.id, on=1)['dashboard']
        return Dashboard(self.__api, dashboard)

    def disable_smart_labels(self):
        dashboard = self.__api.call('dashboards/leave',
                                    id_dashboard=self.id, on=0)['dashboard']
        return Dashboard(self.__api, dashboard)

    def smart_labels(self, value):
        if value is True:
            self.enable_smart_labels()
        else:
            self.disable_smart_labels()

    def delete(self):
        resp = self.__api.call('dashboards/delete',
                                id_dashboard=self.id)['stats']['result']
        return resp == 'TRUE'

    def invite(self, value, message=None):
        from users import User
        kwargs = {}
        if isinstance(value, User):
            kwargs['id_user_to'] = value
            if message:
                kwargs['message'] = message
            dashboard = self.__api.call('dashboards/invite_user_by_id',
                                        **kwargs)['dashboard']
        elif isinstance(value, int):
            kwargs['id_user_to'] = value
            if message:
                kwargs['message'] = message
            dashboard = self.__api.call('dashboards/invite_user_by_id',
                                        **kwargs)['dashboard']
        elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", value) != None:
            kwargs['email'] = value
            if message:
                kwargs['message'] = message
            dashboard = self.__api.call('dashboards/invite_user_by_id',
                                        **kwargs)['dashboard']
        return Dashboard(self.__api, dashboard)

    def needs_upgrade(self):
        """
        Get every dashboard that needs to be upgraded.
        """
        return self.__api.call('dashboards/needs_upgrade',
                                     id_dashboard=self.id)


class Dashboards(object):
    """
    Dashboards give an interface for manage dashboards in Producteev.
    """

    def __init__(self, api):
        self.__api = api

    def new(self, title):
        return Dashboard(self.__api, self.__api.call('dashboards/create',
                                title=title)['dashboard'])

    def get(self, value):
        if isinstance(value, int):
            pass
        elif isinstance(value, Dashboard):
            value = value.id
        elif isinstance(value, str):
            try:
                value = int(str)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None

        dashboard = Dashboard(self.__api,
                                self.__api.call('dashboards/view',
                                id_dashboard=value)['dashboard'])
        return dashboard

    def __list():
        def fget(self):
            dashboards = self.__api.call('dashboards/show_list')['dashboards']
            return [Dashboard(self.__api, x['dashboard']) for x in dashboards]

        def fset(self):
            pass

        return locals()
    list = property(**__list())

    def confirm(self, id_dashboard):
        """
        Confirm invitation for a dashboard.
        """
        if isinstance(id_dashboard, int):
            pass
        elif isinstance(id_dashboard, Dashboard):
            id_dashboard = id_dashboard.id
        elif isinstance(id_dashboard, str):
            try:
                id_dashboard = int(id_dashboard)
            except:
                # TODO: Raise error
                return None
        else:
            # TODO: Raise error
            return None

        dashboards = self.__api.call('dashboards/confirm',
                                     id_dashboard=id_dashboard)['dashboards']
        return [Dashboard(self.__api, x['dashboard']) for x in dashboards]

    def refuse(self, id_dashboard):
        """
        Refuse invitation for a dashboard.
        """
        if isinstance(id_dashboard, int):
            pass
        elif isinstance(id_dashboard, Dashboard):
            id_dashboard = id_dashboard.id
        elif isinstance(id_dashboard, str):
            try:
                id_dashboard = int(id_dashboard)
            except:
                # TODO: Raise error
                return None
        else:
            # TODO: Raise error
            return None

        resp = self.__api.call('dashboards/refuse',
                                id_dashboard=id_dashboard)['stats']['result']
        return resp == 'TRUE'

    def need_upgrade(self):
        """
        Get every dashboard that needs to be upgraded.
        """
        dashboards = self.__api.call('dashboards/need_upgrade_list')['dashboards']
        return [Dashboard(self.__api, x['dashboard']) for x in dashboards]

    def reorder(self, dashboard_list):
        """
        Reorder dashboard position.
        """
        if not isinstance(dashboard_list, list):
            # TODO: raise error
            return None

        dash_list = []
        for dash in dashboard_list:
            if isinstance(dash, int):
                dash_list.append(dash)
            elif isinstance(dash, Dashboard):
                dash_list.append(dash.id)
            elif isinstance(dash, str):
                try:
                    dash = int(dash)
                    dash_list.append(dash)
                except:
                    pass
            else:
                continue

        dashboards = self.__api.call('dashboards/reorder',
                                     id_dashboard=dash_list)['dashboards']
        return [Dashboard(self.__api, x['dashboard']) for x in dashboards]
