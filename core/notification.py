#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

from Queue import Queue
import json

notification_msg_queue = Queue()

class Notification:
    @staticmethod
    def put(obj):
        notification_msg_queue.put(obj)

    @staticmethod
    def get():
        msges = []
        while not notification_msg_queue.empty():
            msges.append(notification_msg_queue.get())
        return json.dumps(msges)
