#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os
import json

class History:
    # STATUS:
    # 1: success
    # 0: fail

    def __init__(self):
        self.log = os.path.join(os.getcwd(), 'cache','hostory.log' )

    def get(self):
        if os.path.exists(self.log):
            with open(self.log) as logf:
                return logf.read()
        else:
            return ''

    def save(self, logcontent):
        if os.path.exists(self.log):
            content = logcontent.split('\r\n')
            with open(self.log, 'w') as kf:
                for idx in range(0,1000):
                    kf.write(content[idx]+'\r\n')
            return json.dumps({'status': 1, 'msg': "Log Saved."})

    def delete(self):
        if os.path.exists(self.log):
            os.remove(self.log)
        return json.dumps({'status': 1, 'msg': "Log Cleared."})
