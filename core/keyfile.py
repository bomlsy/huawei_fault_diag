#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os
import json

class KeyFile:
    # STATUS:
    # 1: success
    # 0: fail

    def __init__(self):
        self.keypath = os.path.join(os.getcwd(),'config', 'keyfile')

    def get(self):
        res = []
        for key in os.listdir(self.keypath):
            with open(os.path.join(self.keypath,key)) as kf:
                res.append({'key':key ,'content': kf.read()})
        return json.dumps(res)

    def add(self, keyfilename, keycontent):
        key = os.path.join(self.keypath, keyfilename)
        if os.path.exists(key):
            return json.dumps({'status':0 ,'msg':'Key %s Exists. Please change filename.' % keyfilename})
        else:
            with open(key,'w') as kf:
                kf.write(keycontent)
            return json.dumps({'status':1,'msg':"Key %s Added." % keyfilename})

    def delete(self, keyfilename):
        key = os.path.join(self.keypath, keyfilename)
        if not os.path.exists(key):
            return json.dumps({'status':0 ,'msg':'Key %s Not Exists' % keyfilename})
        else:
            os.remove(key)
            return json.dumps({'status':1,'msg':"Key %s Deleted." % keyfilename})
