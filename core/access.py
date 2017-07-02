#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os,json
from config import *

class Access:
    # STATUS
    #  1 success
    #  0 config not found
    # -1 parse error
    error = []

    def __init__(self, accessfile):
        try:
            self.user_accessfile = 'config/' + accessfile
            self.full_accessfile = 'cache/full_' + os.path.basename(self.user_accessfile)
            # error as no config
            if not os.path.exists(self.user_accessfile):
                self.status = 0
                return

            # fastload from cache, if config is not updated
            if os.path.exists(self.full_accessfile):
                if os.path.getmtime(self.full_accessfile) > os.path.getmtime(self.user_accessfile):
                    af = open(self.full_accessfile, 'r+')
                    self.access_set = json.load(af)
                    self.status = 1
                    af.close()
                    return

            # standard load and initialization
            af = open(self.user_accessfile, 'r+')
            self.access_set = json.load(af)
            accessid = 0
            for eachone in self.access_set:
                if not eachone.has_key('address'):
                    self.status = 0
                    self.error.append(accessid)
                    return
                if not eachone.has_key('hostname'):
                    eachone['hostname'] = ''
                if not eachone.has_key('port'):
                    eachone['port'] = default_port
                if not eachone.has_key('username'):
                    eachone['username'] = default_username
                if not eachone.has_key('password'):
                    eachone['password'] = default_password
                if not eachone.has_key('authtype'):
                    eachone['authtype'] = default_authtype
                if not eachone.has_key('key'):
                    eachone['key'] = default_key
                eachone['id'] = accessid
                accessid += 1
            self.status = 1
            af.close()
            self.save()
        except:
            self.status = -1

    def save(self):
        try:
            naf = open(self.full_accessfile, 'w+')
            json.dump(self.access_set, naf, indent = 2)
            naf.close()
        except:
            pass
