# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
import logging
from utils import unescape


LOGGER = logging.getLogger('producteev.labels')


class Label(object):
    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_label

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_label

    def __str__(self):
        return self.title

    def __set_title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            label = self.__api.call('labels/set_title.json', id_label=self.id,
                                   title=value)['label']
            self.__reload(label)

        return locals()
    title = property(**__set_title())

    def __tasks():
        def fget(self):
            from tasks import Task
            return [Task(self.__api, x) for x in self.__raw.tasks]

        def fset(self, value):
            pass

        return locals()
    tasks = property(**__tasks())

    def delete(self):
        return self.__api.call('labels/delete.json', id_label=self.id)


class Labels(object):
    def __init__(self, api):
        self.__api = api

    def new(self, title, id_dashboard):
        return Label(self.__api, self.__api.call('labels/create.json',
                            title=title, id_dashboard=id_dashboard)['label'])

    def get(self, id_label):
        return Label(self.__api, self.__api.call('labels/view.json',
                        id_label=id_label)['label'])

    def list(self, **kwargs):
        lables = self.__api.call('labels/show_list.json', **kwargs)['labels']
        return [Label(self.__api, x['label']) for x in lables]
