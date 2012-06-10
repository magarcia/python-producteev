# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
from utils import unescape


class Label(object):
    """
    Label represents an label entity in Producteev.
    """

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__reload(values)

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = int(self.__raw.id_label)

    def __str__(self):
        return self.title

    def __cmp__(self, other):
        return self.id - other.id

    def __set_title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            label = self.__api.call('labels/set_title', id_label=self.id,
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
        resp = self.__api.call('labels/delete',
                                id_label=self.id)['stats']['result']
        return resp == 'TRUE'


class Labels(object):
    """
    Labels give an interface for manage labels in Producteev.
    """

    def __init__(self, api):
        self.__api = api

    def new(self, title, id_dashboard):
        return Label(self.__api, self.__api.call('labels/create',
                            title=title, id_dashboard=id_dashboard)['label'])

    def get(self, id_label):
        if isinstance(id_label, int):
            pass
        elif isinstance(id_label, Label):
            id_label = id_label.id
        elif isinstance(id_label, str):
            try:
                id_label = int(id_label)
            except:
                # TODO: raise error
                return None
        else:
            # TODO: raise error
            return None
        return Label(self.__api, self.__api.call('labels/view',
                        id_label=id_label)['label'])

    def list(self, **kwargs):
        lables = self.__api.call('labels/show_list', **kwargs)['labels']
        return [Label(self.__api, x['label']) for x in lables]
