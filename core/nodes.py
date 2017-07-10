#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


import threading
from Queue import Queue
from time import sleep
import paramiko as ssh
from paramiko.ssh_exception import *
from access import *

# not running directly
if __name__ == '__main__':
    exit(1)



class Node:
    # STATUS
    #  1 connected
    #  0 connecting
    # -1 not connected (normally)
    # -2 access error
    # -3 timeout
    # -4 module error
    status = -1

    def __init__(self, access):
        if isinstance(access, dict):
            self.access = access
            self.status = 0
            self.client = None
            self.chan = None

    def __getitem__(self, item):
        if item == 'id':
            return self.access['id']
        if item == 'status':
            return self.status
        if item == 'hostname':
            return self.access['hostname']

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
                self.client.exec_command('mkdir -p log_analyser')
            threading.Thread(target = self.daemon).start()

        except AuthenticationException:
            self.status = -2
        except (socket.error, NoValidConnectionsError):
            self.status = -3

    def disconnect(self):
        if self.status == 1:
            self.client.exec_command('rm -rf log_analyser')
            self.status = -1
            self.client.close()

    def daemon(self):
        tp = self.client.get_transport()
        while self.status == 1:
            sleep(1)
            if self.status != 1:
                return
            if tp:
                if not tp.is_active():
                    self.status = -3
                    return

    def execute_cmd(self, cmd):
        try:
            stdin,stdout,stderr = self.client.exec_command(cmd)
            res=''
            for line in stdout:
                res+=line
            for line in stderr:
                res+=line
            return res
        except socket.error:
            self.status = -3

    def execute_mod(self, modulename, param=''):
        try:
            mod = open('modules/'+modulename)
            modcontent = mod.read()
            modsave = 'cat > "log_analyser/' + modulename + '" << MOD_EOF\n' + modcontent + '\nMOD_EOF\n'
            self.client.exec_command(modsave)
            self.client.exec_command('chmod +x log_analyser/' + modulename.replace(' ','\\ ')  )
            stdin, stdout, stderr = self.client.exec_command('cd log_analyser && ./' + modulename.replace(' ','\\ ') + ' ' + param )
            res=''
            for line in stdout:
                res+=line
            for line in stderr:
                res+=line
            return res

        except socket.error:
            self.status = -3
        except IOError:
            res = "Module not found"
            return res



class Nodes:
    nodes = []
    connect_threads = []
    disconnect_threads = []
    msg = Queue()
    daemon_run = True

    def getNode(self, nodeid):
        if isinstance(nodeid,str):
            nodeid=int(nodeid)
        for node in self.nodes:
            if node['id'] == nodeid:
                return node
        return None

    def loadNodeList(self, filepath):
        ac = Access(filepath)
        for nodeaccess in ac.access_set:
            node = Node(nodeaccess)
            self.nodes.append(node)
        threading.Thread(target = self.daemon).start()

    def connectAllNodes(self):
        for node in self.nodes:
            th = threading.Thread(target = node.connect)
            self.connect_threads.append(th)
            th.start()

    def disconnectAllNodes(self):
        for node in self.nodes:
            th = threading.Thread(target = node.disconnect)
            self.disconnect_threads.append(th)
            th.start()

    def connectNode(self, nodeid):
        if isinstance(nodeid,str) or isinstance(nodeid,unicode):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            th = threading.Thread(target = node.connect)
            self.connect_threads.append(th)
            th.start()
            return '{"msg":"Node ' + str(nodeid) +': ' + node['hostname'] + ' Connecting"}'
        else:
            return '{"msg":"ERROR: Wrong Node ID"}'

    def disconnectNode(self, nodeid):
        if isinstance(nodeid,str) or isinstance(nodeid,unicode):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            th = threading.Thread(target = node.disconnect)
            self.disconnect_threads.append(th)
            th.start()
            return '{"msg":"Node ' + str(nodeid) +': ' + node['hostname'] + ' Disconnecting"}'
        else:
            return '{"msg":"ERROR: Wrong Node ID"}'

    def getBasicStatus(self, nodeid):
        if isinstance(nodeid,str) or isinstance(nodeid,unicode):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            state = {}
            state['hostname'] = node.access['hostname']
            state['id'] = node['id']
            state['status'] = node['status']
            return json.dumps(state)
        else:
            return '{}'

    def getAllBasicStatus(self):
        states = []
        for node in self.nodes:
            state = {}
            state['hostname'] = node.access['hostname']
            state['id'] = node.access['id']
            state['status'] = node.status
            states.append(state)
        return json.dumps(states)

    def getDetailedStatus(self, nodeid):
        if isinstance(nodeid,str) or isinstance(nodeid,unicode):
            nodeid=int(nodeid)
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
            state['id'] = node['id']
            state['status'] = node['status']
            state['username'] = node.access['username']
            state['authtype'] = node.access['authtype']
            state['address'] = node.access['address']
            state['port'] = node.access['port']
            states.append(state)
        return json.dumps(states)

    # async
    def executeCmd(self, nodeid, cmd):
        node = self.getNode(nodeid)
        if node and node['status'] == 1:
            res = node.execute_cmd(cmd)
            self.msg.put({'event': 'execute_cmd', 'content': {'command': cmd, 'result': res }, 'node':nodeid})
            return '{"msg":"success"}'
        else:
            return '{"msg":"no such node or node not running"}'

    def executeCmdAll(self, cmd):
        for node in self.nodes:
            if node['status'] == 1:
                res = node.execute(cmd)
                self.msg.put({'event': 'execute_cmd', 'content': {'command': cmd, 'result': res }, 'node': node['id']})
        return '{"msg":"success"}'

    def executeMod(self, nodeid, mod, param=''):
        node = self.getNode(nodeid)
        if node and node['status'] == 1:
            res = node.execute_mod(mod,param)
            self.msg.put({'event': 'execute_mod', 'content': {'module': mod, 'result': res }, 'node': node['id']})
            return '{"msg":"success"}'
        else:
            return '{"msg":"no such node or node not running"}'

    def executeModAll(self, mod, param=''):
        for node in self.nodes:
            if node['status'] == 1:
                res = node.execute_mod(mod,param)
                self.msg.put({'event': 'execute_mod', 'content': {'module': mod, 'result': res }, 'node': node['id']})
        return '{"msg":"success"}'


    def daemon(self):
        while self.daemon_run:
            last_status = json.loads(self.getAllBasicStatus())
            sleep(status_daemon_interval)
            for eachstatus in last_status:
                node = self.getNode(eachstatus['id'])
                if node['status'] != eachstatus['status'] or node['hostname'] != eachstatus['hostname']:
                    msg_update = {'event': 'update', 'id': eachstatus['id'],
                                  'content': json.loads(self.getBasicStatus(eachstatus['id']))}
                    self.msg.put(msg_update)


    def stopdaemon(self):
        self.daemon_run=False

    def getNotification(self):
        msges = []
        while not self.msg.empty():
            msges.append(self.msg.get())
        return json.dumps(msges)
