#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os
import json
import threading
import paramiko as ssh
from time import sleep
from paramiko.ssh_exception import *
from config import *

# not running directly
if __name__ == '__main__':
    exit(1)


class Event:
    # called by web.py
    # async
    # push request to queue and hang on, wait response from EventProxy
    pass


class EventProxy:
    # running in background
    # use queue
    pass


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


class Nodes:
    nodes = []
    connect_threads = []

    def getNode(self, nodeid):
        for node in self.nodes:
            if node['id'] == nodeid:
                return node
        return None

    def loadNodeList(self, filepath):
        ac = Access(filepath)
        for nodeaccess in ac.access_set:
            node = Node(nodeaccess)
            self.nodes.append(node)

    def connectAllNodes(self):
        for node in self.nodes:
            th = threading.Thread(target = node.connect())
            self.connect_threads.append(th)
            th.start()

    def disconnectAllNodes(self):
        for node in self.nodes:
            node.disconnect()

    def connectNode(self, nodeid):
        node = self.getNode(nodeid)
        if node:
            th = threading.Thread(target = node.connect())
            self.connect_threads.append(th)
            th.start()

    def disconnectNode(self, nodeid):
        node = self.getNode(nodeid)
        if node:
            node.disconnect()

    def getBasicStatus(self, nodeid):
        node = self.getNode(nodeid)
        if node:
            state = {}
            state['hostname'] = node.access['hostname']
            state['id'] = node.access['id']
            state['status'] = node.access['status']
            return json.dumps(state)
        else:
            return '{}'

    def getAllBasicStatus(self):
        states = []
        for node in self.nodes:
            state = {}
            state['hostname'] = node.access['hostname']
            state['id'] = node.access['id']
            state['status'] = node.access['status']
            states.append(state)
        return json.dumps(states)

    def getDetailedStatus(self, nodeid):
        node = self.getNode(nodeid)
        if node:
            state = {}
            state['hostname'] = node.access['hostname']
            state['id'] = node.access['id']
            state['status'] = node.status
            state['username'] = node.access['username']
            state['authtype'] = node.access['authtype']
            state['address'] = node.access['address']
            state['port'] = node.access['port']
            return json.dumps(state)
        else:
            return '{}'

    def getAllDetailedStatus(self):
        states = []
        for node in self.nodes:
            state = {}
            state['hostname'] = node.access['hostname']
            state['id'] = node.access['id']
            state['status'] = node.status
            state['username'] = node.access['username']
            state['authtype'] = node.access['authtype']
            state['address'] = node.access['address']
            state['port'] = node.access['port']
            states.append(state)
        return json.dumps(states)

    def executeCmd(self, cmd, nodeid):
        node = self.getNode(nodeid)
        res = ''
        if node:
            res = node.execute(cmd)
        return json.dumps({'result': res})

    # block. deprecated
    def executeCmdAll(self, cmd):
        results = []
        for node in self.nodes:
            res = node.execute(cmd)
            results.append({'id': node.access['id'], 'result': res})
        return json.dumps(results)


class Node:
    # STATUS
    #  1 connected
    #  0 connecting
    # -1 not connected (normally)
    # -2 access error
    # -3 timeout
    status = -1

    def __init__(self, access):
        if isinstance(access, dict):
            self.access = access
            self.status = 0
            self.client = None

    def connect(self):
        try:
            if self.status != 1:
                self.client = ssh.SSHClient()
                self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())
                if self.access['authtype'] == 'key':
                    self.client.connect(hostname = self.access['address'], port = self.access['port'],
                                        username = self.access['username'], key_filename = self.access['key'],
                                        password = self.access['password'])
                elif self.access['authtype'] == 'password':
                    self.client.connect(hostname = self.access['address'], port = self.access['port'],
                                        username = self.access['username'], password = self.access['password'])

                stdin, stdout, stderr = self.client.exec_command('hostname')
                for line in stdout:
                    self.access['hostname'] = line.strip('\n')
                    break
                self.status = 1
            self.daemon()

        except AuthenticationException:
            self.status = -2
        except (socket.error, NoValidConnectionsError):
            self.status = -3

    def disconnect(self):
        if self.status == 1:
            self.client.close()
            self.status = -1

    def daemon(self):
        def mission():
            tp = self.client.get_transport()
            while self.status == 1:
                sleep(5)
                print 'running daemon'
                if tp:
                    if not tp.is_active():
                        self.status = -3
                        break

        threading.Thread(target = mission()).start()

    def execute_cmd(self, cmd):
        try:
            ioe = self.client.exec_command(cmd)
            res = ''
            for line in ioe[1]:
                res = res + line
            for line in ioe[2]:
                res = res + line
            return res
        except socket.error:
            self.status = -3

    def execute_module(self, modulename):
        try:
            ioe = self.client.exec_command(modulename)
        except socket.error:
            self.status = -3

    def ctrl_c(self):
        try:
            ioe = self.client.exec_command('\x03')
        except socket.error:
            self.status = -3
