# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
from utils import unescape
import logging


LOGGER = logging.getLogger('producteev.subtasks')


class Subtask(object):

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_subtask
        LOGGER.debug(self.__raw.__dict__)

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_subtask

    def __str__(self):
        return self.title

    def __title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            subtask = self.__api.call('subtasks/set_title.json', id_subtask=self.id,
                                   title=value)['subtask']
            self.__reload(subtask)

        return locals()
    title = property(**__title())

    def __position():
        def fget(self):
            return self.__raw.position

        def fset(self, value):
            subtask = self.__api.call('subtasks/set_position.json',
                                      id_subtask=self.id)['subtask']
            self.__reload(subtask)

        return locals()
    position = property(**__position())

    def delete(self):
        return self.__api.call('subtasks/delete.json', id_subtask=self.id)


class Subtasks(object):
    def __init__(self, api):
        self.__api = api

    def new(self, task, title):
        from tasks import Task
        if isinstance(task, int):
            subtask = self.__api.call('subtasks/create.json', id_task=task,
                                   title=title)['subtask']
        elif isinstance(task, Task):
            subtask = self.__api.call('subtasks/create.json', id_task=task.id,
                                   title=title)['subtask']
        else:
            subtask = None

        return Subtask(self.__api, subtask)
