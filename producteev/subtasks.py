# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
from utils import unescape


class Subtask(object):
    """
    Subtask represents an subtask entity in Producteev.
    """

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__reload(values)

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = int(self.__raw.id_subtask)

    def __str__(self):
        return self.title

    def __cmp__(self, other):
        return self.id - other.id

    def __title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            subtask = self.__api.call('subtasks/set_title', id_subtask=self.id,
                                   title=value)['subtask']
            self.__reload(subtask)

        return locals()
    title = property(**__title())

    def __position():
        def fget(self):
            return self.__raw.position

        def fset(self, value):
            subtask = self.__api.call('subtasks/set_position',
                                      id_subtask=self.id)['subtask']
            self.__reload(subtask)

        return locals()
    position = property(**__position())

    def delete(self):
        resp = self.__api.call('subtasks/delete',
                               id_subtask=self.id)['stats']['result']
        return resp == 'TRUE'


class Subtasks(object):
    """
    Subtasks give an interface for manage subtasks in Producteev.
    """

    def __init__(self, api):
        self.__api = api

    def new(self, task, title):
        from tasks import Task
        if isinstance(task, int):
            pass
        elif isinstance(task, Task):
            task = task.id
        elif isinstance(task, str):
            try:
                task = int(task)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None

        subtask = self.__api.call('subtasks/create', id_task=task,
                                   title=title)['subtask']

        return Subtask(self.__api, subtask)
