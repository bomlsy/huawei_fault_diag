#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

from Queue import Queue
import json

notification_queue_update = Queue()
notification_queue_cmd = Queue()
notification_queue_mod = Queue()

class Notification:
    @staticmethod
    def put(event,obj):
        queue_target = None
        if event == 'update':
            queue_target = notification_queue_update
        if event == 'cmd':
            queue_target = notification_queue_cmd
        if event == 'mod':
            queue_target = notification_queue_mod

        if queue_target:
            queue_target.put(obj)

    @staticmethod
    def get(event):
        msges = []

        queue_target = None
        if event == 'update':
            queue_target = notification_queue_update
        if event == 'cmd':
            queue_target = notification_queue_cmd
        if event == 'mod':
            queue_target = notification_queue_mod

        if queue_target:
            while not queue_target.empty():
                msges.append(queue_target.get())
            return json.dumps(msges)
