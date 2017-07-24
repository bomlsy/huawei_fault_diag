#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os,json
import threading
from time import sleep

from config import *
from notification import Notification

cache_ready2save = False

def SetCacheReady2Save(tf):
    global cache_ready2save
    cache_ready2save = tf


class Access:

    def __init__(self):
        self._iter_id = 0
        self.status = 0
        self.user_access_set = []
        self.full_access_set = []
        self.accessfile = ""
        self.user_accessfile = ""
        self.full_accessfile = ""
        self.daemon_run = True
        th = threading.Thread(target = self.daemon)
        th.daemon=True
        th.start()


    def _load_single_access(self,access, id_AI=True):   # id_AutoIncreasement
        if isinstance(access,unicode) or isinstance(access,str):
            try:
                access = json.load(access)
            except:
                return

        if not isinstance(access,dict):
            return

        full_access = access.copy()

        if not access.has_key('address'):
            return
        if not access.has_key('hostname'):
            full_access['hostname'] = ''
        if not access.has_key('port'):
            full_access['port'] = default_port
        if not access.has_key('username'):
            full_access['username'] = default_username
        if not access.has_key('password'):
            full_access['password'] = default_password
        if not access.has_key('authtype'):
            full_access['authtype'] = default_authtype
        if not access.has_key('key'):
            full_access['key'] = default_key

        if id_AI:
            full_access['id'] = self._iter_id
            self._iter_id += 1

        return full_access

    def addAccess(self,ac):
        if ac.has_key('address') and (
                    ac.has_key('password') or (
                    ac.has_key('authtype') and ac.get('authtype')=='key' and ac.has_key('key'))):
            self.user_access_set.append(ac)
            full_ac = self._load_single_access(ac)
            self.full_access_set.append(full_ac)
            self.save()
            self.save_cache()
            return full_ac

    def delAccess(self,nodeid):
        if isinstance(nodeid,unicode) or isinstance(nodeid,str):
            nodeid = int(nodeid)
        for index,full_ac in enumerate(self.full_access_set):
            if full_ac['id'] == nodeid:
                del self.user_access_set[index]
                del self.full_access_set[index]
                self.save()
                self.save_cache()
                return True
        return False

    def updateAccess(self,nodeid,access_json):
        new_uac=access_json
        if isinstance(nodeid, unicode):
            nodeid = int(nodeid)
        for index,full_ac in enumerate(self.full_access_set):
            if full_ac['id'] == nodeid:
                if new_uac.has_key('address') and (
                            new_uac.has_key('password') or (
                            new_uac.has_key('authtype') and new_uac.get('authtype')=='key' and new_uac.has_key('key'))):
                    self.user_access_set[index] = new_uac
                    new_fac = self._load_single_access(new_uac, id_AI = False)
                    full_ac = new_fac
                    self.save()
                    self.save_cache()
                    return full_ac


    def load(self, accessfile):
        try:
            self.accessfile = accessfile
            self.user_accessfile = os.path.join('config', self.accessfile)
            self.full_accessfile = os.path.join('cache', 'full_'+os.path.basename(self.user_accessfile))
            # error as no such config
            if not os.path.exists(self.user_accessfile):
                return

            # fastload from cache, if config is not updated
            if os.path.exists(self.full_accessfile):
                if os.path.getmtime(self.full_accessfile) > os.path.getmtime(self.user_accessfile):
                    faf = open(self.full_accessfile, 'r+')
                    uaf = open(self.user_accessfile, 'r+')
                    self.full_access_set = json.load(faf)
                    self.user_access_set = json.load(uaf)
                    for id_ac in self.full_access_set:
                        if self._iter_id < id_ac['id']:
                            self._iter_id = id_ac['id']
                    self._iter_id +=1
                    uaf.close()
                    faf.close()
                    return

            # standard load and initialization
            af = open(self.user_accessfile, 'r+')
            self.user_access_set = json.load(af)
            for eachone in self.user_access_set:
                self.full_access_set.append(self._load_single_access(eachone))
            af.close()
            self.save_cache()
        except:
            pass

    def save(self):
        try:
            uaf = open(self.user_accessfile, 'w+')
            json.dump(self.user_access_set, uaf, indent = 2)
            uaf.close()
        except:
            pass

    def save_cache(self):
        try:
            faf = open(self.full_accessfile, 'w+')
            json.dump(self.full_access_set, faf, indent = 2)
            faf.close()
        except:
            pass

    def daemon(self):
        while self.daemon_run:
            sleep(cache_daemon_interval)
            global cache_ready2save
            if cache_ready2save:
                cache_ready2save = False
                self.save_cache()

    def stopdaemon(self):
        self.daemon_run=False
