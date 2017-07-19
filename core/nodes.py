#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


import paramiko as ssh
from paramiko.ssh_exception import *
from access import *
from notification import Notification

# not running directly
if __name__ == '__main__':
    exit(1)


class Node:
    # STATUS
    #  1 connected
    #  0 connecting
    # -1 disconnected (normally)
    # -2 access error
    # -3 timeout
    status = -1

    def __init__(self, config):
        if isinstance(config, dict):
            self.config = config
            self.status = 0
            self.client = None
            self.chan = None
            self.msg = Notification()

    def __getitem__(self, item):
        if item == 'id':
            return self.config['id']
        if item == 'status':
            return self.status
        if item == 'hostname':
            return self.config['hostname']

    def connect(self):
        try:
            if self.status != 1:
                self.client = ssh.SSHClient()
                self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())
                if self.config['authtype'] == 'key':
                    self.client.connect(hostname = self.config['address'], port = self.config['port'],
                                        username = self.config['username'], key_filename = os.path.join(os.getcwd(),'config','keyfile',self.config['key']),
                                        password = self.config['password'])
                elif self.config['authtype'] == 'password':
                    self.client.connect(hostname = self.config['address'], port = self.config['port'],
                                        username = self.config['username'], password = self.config['password'])

                stdin, stdout, stderr = self.client.exec_command('hostname')
                for line in stdout:
                    self.config['hostname'] = line.strip('\n')
                    break
                SetCacheReady2Save(True)

                self.status = 1
                self.client.exec_command('mkdir -p log_analyser')
                th = threading.Thread(target = self.daemon)
                th.daemon=True
                th.start()
                # push notification
                self.msg.put('update',self.getBasicStatus())

        except AuthenticationException:
            self.status = -2
        except:
            self.status = -3

    def disconnect(self):
        if self.status == 1:
            self.status = -1
            self.client.exec_command('rm -rf log_analyser')
            self.client.close()
            # push notification
            self.msg.put('update', self.getBasicStatus())


    def getBasicStatus(self):
        state = {}
        state['hostname'] = self['hostname']
        state['address'] = self.config['address']
        state['id'] = self['id']
        state['status'] = self['status']
        return state


    def getDetailStatus(self):
        state = {}
        state['hostname'] = self['hostname']
        state['id'] = self['id']
        state['status'] = self['status']
        state['username'] = self.config['username']
        state['authtype'] = self.config['authtype']
        state['address'] = self.config['address']
        state['port'] = self.config['port']
        return state

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
    # block
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

    # block
    def execute_mod(self, modulename, param=''):
        try:
            mod = open(os.path.join('modules',modulename))
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
    access = None
    nodes = []
    connect_threads = []
    disconnect_threads = []
    msg = Notification()


    def daemon(self):
        while True:
            sleep(20)
            for idx in range(len(self.connect_threads)-1,0,-1):
                if not self.connect_threads[idx].isAlive():
                    del self.connect_threads[idx]
            for idx in range(len(self.disconnect_threads)-1,0,-1):
                if not self.disconnect_threads[idx].isAlive():
                    del self.disconnect_threads[idx]

    def addNode(self,access_str):
        full_ac = self.access.addAccess(access_str)
        if full_ac:
            self.nodes.append(Node(full_ac))
            return full_ac['id']
        else:
            return -1

    def delNode(self,nodeid):
        node = self.getNode(nodeid)
        if node:
            self.nodes.remove(node)
            return self.access.delAccess(nodeid)
        else:
            return False

    def updateNode(self,nodeid,access_str):
        full_ac = self.access.updateAccess(nodeid, access_str)
        if full_ac:
            if isinstance(nodeid, unicode) or isinstance(nodeid, str):
                nodeid=int(nodeid)
            for index,node in enumerate(self.nodes):
                if node['id'] == nodeid:
                    node.disconnect()
                    self.nodes[index] = Node(full_ac)
                    return True
        return False

    def getNode(self, nodeid):
        if isinstance(nodeid, unicode) or isinstance(nodeid, str):
            nodeid=int(nodeid)
        for node in self.nodes:
            if node['id'] == nodeid:
                return node
        return None

    def loadAccess(self, filepath):
        self.access = Access()
        self.access.load(filepath)
        for nodeaccess in self.access.full_access_set:
            node = Node(nodeaccess)
            self.nodes.append(node)
        th = threading.Thread(target=self.daemon)
        th.daemon=True
        th.start()

    def connectAllNodes(self):
        for node in self.nodes:
            th = threading.Thread(target = node.connect)
            self.connect_threads.append(th)
            th.daemon=True
            th.start()

    def disconnectAllNodes(self):
        for node in self.nodes:
            th = threading.Thread(target = node.disconnect)
            self.disconnect_threads.append(th)
            th.daemon=True
            th.start()

    def connectNode(self, nodeid):
        if isinstance(nodeid, unicode) or isinstance(nodeid, str):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            th = threading.Thread(target = node.connect)
            self.connect_threads.append(th)
            th.daemon=True
            th.start()
            return '{"msg":"Node ' + str(nodeid) +': ' + node['hostname'] + ' Connecting"}'
        else:
            return '{"msg":"ERROR: Wrong Node ID"}'

    def disconnectNode(self, nodeid):
        if isinstance(nodeid, unicode) or isinstance(nodeid, str):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            th = threading.Thread(target = node.disconnect)
            self.disconnect_threads.append(th)
            th.daemon=True
            th.start()
            return '{"msg":"Node ' + str(nodeid) +': ' + node['hostname'] + ' Disconnecting"}'
        else:
            return '{"msg":"ERROR: Wrong Node ID"}'

    def getBasicStatus(self, nodeid):
        if isinstance(nodeid, unicode) or isinstance(nodeid, str):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            return json.dumps(node.getBasicStatus())
        else:
            return '{"id":%d, "msg":"No such node %d"}' % (nodeid,nodeid)

    def getAllBasicStatus(self):
        states = []
        for node in self.nodes:
            states.append(node.getBasicStatus())
        return json.dumps(states)

    def getDetailStatus(self, nodeid):
        if isinstance(nodeid, unicode) or isinstance(nodeid, str):
            nodeid=int(nodeid)
        node = self.getNode(nodeid)
        if node:
            return json.dumps(node.getDetailStatus())
        else:
            return '{"id":%d, "msg":"No such node %d"}' % (nodeid, nodeid)

    def getAllDetailStatus(self):
        states = []
        for node in self.nodes:
            states.append(node.getDetailStatus())
        return json.dumps(states)

    def executeCmd(self, nodeid, cmd):
        node = self.getNode(nodeid)
        if node and node['status'] == 1:
            def task():
                res = node.execute_cmd(cmd)
                self.msg.put('cmd',{'command': cmd, 'result': res , 'nodeid':nodeid})
            th = threading.Thread(target = task)
            th.daemon=True
            th.start()
            return '{"id":%d, "msg":"Cmd `%s` sent to %d "}' % (nodeid ,cmd , nodeid)
        else:
            return '{"id":%d, "msg":"No such node %d or node not running"}' % (nodeid, nodeid)

    def executeCmdAll(self, cmd):
        for node in self.nodes:
            def task():
                res = node.execute_cmd(cmd)
                self.msg.put('cmd', {'command': cmd, 'result': res, 'nodeid': node['id']})
            th = threading.Thread(target = task)
            th.daemon=True
            th.start()
        return '{"id":"all", "msg":"Cmd `%s` sent to all nodes"}' % cmd

    def executeMod(self, nodeid, mod, param=''):
        node = self.getNode(nodeid)
        if node and node['status'] == 1:
            def task():
                res = node.execute_mod(mod, param)
                self.msg.put('mod', {'command': mod, 'result': res, 'nodeid': nodeid})
            th = threading.Thread(target = task)
            th.daemon=True
            th.start()
            return '{"id":%d, "msg":"Module `%s` executed on %d "}' % (nodeid ,mod , nodeid)
        else:
            return '{"msg":"no such node or node not running"}'

    def executeModAll(self, mod, param=''):
        for node in self.nodes:
            if node['status'] == 1:
                def task():
                    res = node.execute_mod(mod, param)
                    self.msg.put('mod', {'command': mod, 'result': res, 'nodeid': node['id']})
                th = threading.Thread(target = task)
                th.daemon = True
                th.start()
        return '{"id":"all", "msg":"Module `%s` executed on all noeds"}' % mod

