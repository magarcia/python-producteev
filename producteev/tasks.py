# Copyright (c) 2012 Martin Garcia <newluxfero@gmail.com>
#
# This file is part of python-producteev, and is made available under
# MIT license. See LICENSE for the full details.
import logging
from utils import unescape

STATUS = ('UNDONE', 'DONE')


# TODO:
# tasks/note_view
# tasks/notes_get
# tasks/note_create
# tasks/note_delete
# tasks/activity_view
# tasks/activities_get
# tasks/subtasks

LOGGER = logging.getLogger('producteev.tasks')


class Task(object):

    class __raw:
            pass

    def __init__(self, api, values):
        self.__api = api
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_task

    def __reload(self, values):
        self.__raw.__dict__.update(values)
        self.id = self.__raw.id_task

    def __str__(self):
        return self.title

    def __set_title():
        def fget(self):
            return unescape(self.__raw.title)

        def fset(self, value):
            task = self.__api.call('tasks/set_title.json', id_task=self.id,
                                   title=value)['task']
            self.__reload(task)

        return locals()
    title = property(**__set_title())

    def __set_status():
        def fget(self):
            return STATUS[int(self.__raw.status) - 1]

        def fset(self, value):
            if isinstance(value, int):
                task = self.__api.call('tasks/set_status.json',
                                        id_task=self.id,
                                        status=value)['task']
            elif isinstance(value, str):
                try:
                    value = int(value)
                    task = self.__api.call('tasks/set_status.json',
                                            id_task=self.id,
                                            status=value)['task']
                except:
                    try:
                        value = STATUS.index(value.upper()) + 1
                        task = self.__api.call('tasks/set_status.json',
                                                id_task=self.id,
                                                status=value)['task']
                    except:
                        task = None
            if not task:
                self.__reload(task)
        return locals()
    status = property(**__set_status())

    def __set_star():
        def fget(self):
            return self.__raw.star

        def fset(self, value):
            task = self.__api.call('tasks/set_star.json', id_task=self.id,
                                    star=value)['task']
            self.__reload(task)
        return locals()
    star = property(**__set_star())

    def __responsible():
        def fget(self):
            from users import User
            return User(self.__api, self.__raw.id_responsible)

        def fset(self, value):
            from users import User
            if isinstance(value, int):
                task = self.__api.call('tasks/set_responsible.json',
                                       id_task=self.id,
                                       id_responsible=value)['task']
            elif isinstance(value, User):
                task = self.__api.call('tasks/set_responsible.json',
                                       id_task=self.id,
                                       id_responsible=value.id)['task']
            elif value is None:
                task = self.__api.call('tasks/unset_responsible.json',
                                       id_task=self.id)['task']
            self.__reload(task)
        return locals()
    responsible = property(**__responsible())

    def __set_deadline():
        def fget(self):
            if self.__raw.deadline == '':
                return None
            else:
                from datetime import datetime
                from core import PRODUCTEEV_DATE_FORMAT
                return datetime.strptime(
                    ' '.join(self.__raw.deadline.split(' ')[0:-1]),
                    PRODUCTEEV_DATE_FORMAT)

        def fset(self, value):
            if value:
                task = self.__api.call('tasks/set_deadline.json',
                                       id_task=self.id,
                                       deadline=value)['task']
            else:
                task = self.__api.call('tasks/unset_deadline.json',
                                       id_task=self.id)['task']
            self.__reload(task)
        return locals()
    deadline = property(**__set_deadline())

    def __set_reminder():
        def fget(self):
            return self.__raw.reminder

        def fset(self, value):
            if value:
                task = self.__api.call('tasks/set_reminder.json',
                                        id_task=self.id, reminder=value)['task']
            else:
                task = self.__api.call('tasks/set_reminder.json',
                                        id_task=self.id, reminder=0)['task']
            self.__reload(task)

        return locals()
    reminder = property(**__set_reminder())

    def __set_repeating():
        def fget(self):
            return self.__raw.repeating_interval, self.__raw.repeating_value

        def fset(self, value, interval=1):
            if value:
                task = self.__api.call('tasks/set_repeating.json',
                                       id_task=self.id,
                                       repeating_interval=interval,
                                       repeating_value=value)['task']
            else:
                task = self.__api.call('tasks/unset_repeating.json',
                                       id_task=self.id)['task']
            self.__reload(task)
        return locals()
    repeating = property(**__set_repeating())

    def delete(self):
        return self.__api.call('tasks/delete.json', id_task=self.id)

    def __set_labels():
        def fget(self):
            from labels import Label
            return [Label(self.__api, x['label']) for x in self.__raw.labels]

        def fset(self, value):
            # TODO: tasks/change_labels
            pass
        return locals()
    labels = property(**__set_labels())

    def __set_workspace():
        def fget(self):
            return self.__api(int(self.__raw.id_dashboard))

        def fset(self, value):
            from dashboards import Dashboard
            if isinstance(value, int):
                task = self.__api.call('tasks/set_workspace.json',
                                        id_task=self.id,
                                        id_dashboard=value)['task']
            elif isinstance(value, Dashboard):
                task = self.__api.call('tasks/set_workspace.json',
                                        id_task=self.id,
                                        id_dashboard=value.id)['task']
            else:
                task = None
            if not task:
                self.__reload(task)
        return locals()
    dashboard = property(**__set_workspace())

    # TODO: Add support for notes
    # TODO: Add support for activities

    def __get_subtasks():
        def fget(self):
            from subtasks import Subtask
            return [Subtask(self.__api, x) for x in self.__raw.subtasks]

        def fset(self, value):
            pass
        return locals()
    subtasks = property(**__get_subtasks())


class Tasks(object):
    def __init__(self, api):
        self.__api = api

    def new(self, title, **kwargs):
        """
        """
        return Task(self.__api, self.__api.call('tasks/create.json', title=title,
                                   **kwargs)['task'])

    def get(self, id_task, **kwargs):
        """
        """
        return Task(self.__api, self.__api.call('tasks/view.json', id_task=id_task,
                             **kwargs)['task'])

    def list(self, **kwargs):
        """
        """
        tasks = self.__api.call('tasks/my_tasks.json', **kwargs)['tasks']
        return [Task(self.__api, x['task']) for x in tasks]

    def list_all(self, **kwargs):
        """
        """
        tasks = self.__api.call('tasks/show_list.json', **kwargs)['tasks']
        return [Task(self.__api, x['task']) for x in tasks]

    def archived(self, **kwargs):
        tasks = self.__api.call('tasks/archived.json', **kwargs)['tasks']
        return [Task(self.__api, x['task']) for x in tasks]

    def list_team(self, **kwargs):
        tasks = self.__api.call('tasks/my_team_tasks.json', **kwargs)['tasks']
        return [Task(self.__api, x['task']) for x in tasks]
