# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.


class Activity(object):
    """
    Activity represents an activity entity in Producteev.
    """

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__reload(values)

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = int(self.__raw.id_activity)

    def __cmp__(self, other):
        return self.id - other.id

    def set_read(self):
        """
        Set activity status as read.
        """
        activities = self.__api.call('activities/set_read',
                                     id_activity=self.id)['activities']
        return [Activity(self.__api, x['activity']) for x in activities]


class Activities(object):
    """
    Activities give an interface for manage activities in Producteev.
    """

    def __init__(self, api):
        self.__api = api

    def __list():
        """
        Get activities. Don't return activities older than 1 month.
        """
        def fget(self):
            activities = self.__api.call('activities/show_activities')['activities']
            return [Activity(self.__api, x['activity']) for x in activities]

        def fset(self):
            pass

        return locals()
    list = property(**__list())

    def get(self, id_activity):
        """
        Get activity.
        """
        if isinstance(id_activity, int):
            pass
        elif isinstance(id_activity, Activity):
            id_activity = id_activity.id
        elif isinstance(id_activity, str):
            try:
                id_activity = int(id_activity)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None

        activity = self.__api.call('tasks/activity_view')['activity']
        return Activity(self.__api, activity)

    def __notifications():
        """
        Get every notifications (notifications are activities that current user
        is concerned about). Don't return notifications older than 1 month.
        """
        def fget(self):
            activities = self.__api.call('activities/show_notifications')['activities']
            return [Activity(self.__api, x['activity']) for x in activities]

        def fset(self):
            # TODO: raise inmutable object
            pass

        return locals()
    notifications = property(**__notifications())

    def set_notifications_read(self, id_dashboard, last_id):
        """
        Set notifications status as read.
        """
        from dashboards import Dashboard
        if isinstance(id_dashboard, int):
            pass
        elif isinstance(id_dashboard, Dashboard):
            id_dashboard = id_dashboard.id
        elif isinstance(id_dashboard, str):
            try:
                id_dashboard = int(id_dashboard)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None

        if isinstance(last_id, int):
            pass
        elif isinstance(last_id, Activity):
            last_id = last_id.id
        elif isinstance(last_id, str):
            try:
                last_id = int(last_id)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None

        activities = self.__api.call('activities/notifications_set_read',
                                     id_dashboard=id_dashboard,
                                     last_id=last_id)['activities']
        return [Activity(self.__api, x['activity']) for x in activities]

    def set_activities_read(self, activities_list):
        """
        Set activities status as read.
        """
        if not isinstance(activities_list, list):
            # TODO: raise error
            return None

        act_list = []
        for act in activities_list:
            if isinstance(act, int):
                act_list.append(act)
            elif isinstance(act, Activity):
                act_list.append(act.id)
            elif isinstance(act, str):
                try:
                    act = int(act)
                    act_list.append(act)
                except:
                    pass
            else:
                continue

        activities = self.__api.call('activities/set_read',
                                     id_activity=act_list)['activities']
        return [Activity(self.__api, x['activity']) for x in activities]
