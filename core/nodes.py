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
    # -3 Timeout (tcp drop)
    # -4 Port Refused  (tcp reject)
    # -5 Network is unreachable (no route to host)
    status = -1

    def __init__(self):
            self.client = None
            self.config = None
            self.msg = Notification()
            self.status = -1

    def loadConfig(self,config):
        if isinstance(config, dict):
            self.config = config

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
                    self.client.connect(hostname = self.config['address'], port = int(self.config['port']),
                                        username = self.config['username'], key_filename = os.path.join(os.getcwd(),'config','keyfile',self.config['key']),
                                        password = self.config['password'], timeout = tcp_connect_timeout)
                elif self.config['authtype'] == 'password':
                    self.client.connect(hostname = self.config['address'], port = int(self.config['port']),
                                        username = self.config['username'], password = self.config['password'],  timeout = tcp_connect_timeout)

                stdin, stdout, stderr = self.client.exec_command('hostname')
                for line in stdout:
                    self.config['hostname'] = line.strip('\n')
                    break
                SetCacheReady2Save(True)

                self.status = 1
                self.client.exec_command('mkdir -p log_analyser', timeout=command_timeout)


        except AuthenticationException:
            self.status = -2
        except (socket.timeout, SSHException):
            self.status = -3
        except NoValidConnectionsError:
            self.status = -4
        except socket.error:
            self.status = -5
        finally:
            # push notification
            self.msg.put('update', self.getBasicStatus())


    def disconnect(self):
        if self.status == 1:
            self.status = -1
            try:
                self.client.exec_command('rm -rf log_analyser', timeout=command_timeout)
                self.client.close()
            except (socket.timeout, SSHException):
                self.status = -3.
            except socket.error:
                self.status = -5
            finally:
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
        if state['authtype']  == 'key':
           state['key'] = self.config['key']
        return state

    # block
    def execute_cmd(self, cmd):
        res = ''
        try:
            stdin,stdout,stderr = self.client.exec_command(cmd, timeout=command_timeout)
            for line in stdout:
                res+=line
            for line in stderr:
                res+=line
        except (socket.timeout, SSHException):
            self.status = -3
            self.msg.put('update', self.getBasicStatus())
        except socket.error:
            self.status = -5
            self.msg.put('update', self.getBasicStatus())
        finally:
            return res

    # block
    def execute_mod(self, modulename, param=''):
        res = ''
        try:
            mod = open(os.path.join('modules',modulename))
            modcontent = mod.read()
            modsave = 'cat > "log_analyser/' + modulename + '" << MOD_EOF\n' + modcontent.replace("$","\\$") + '\nMOD_EOF\n'
            self.client.exec_command(modsave, timeout=command_timeout)
            self.client.exec_command('chmod +x log_analyser/"' + modulename + '"' , timeout=command_timeout )
            stdin, stdout, stderr = self.client.exec_command('cd log_analyser && ./"' + modulename + '" ' + param, timeout=command_timeout )
            for line in stdout:
                res+=line
            for line in stderr:
                res+=line
        except (socket.timeout, SSHException):
            self.status = -3
            self.msg.put('update', self.getBasicStatus())
        except socket.error:
            self.status = -5
            self.msg.put('update', self.getBasicStatus())
        except IOError:
            res = "Module not found"
        finally:
            return res



class Nodes:
    access = None
    nodes = []
    connect_threads = []
    disconnect_threads = []
    msg = Notification()
    daemon_run = True

    def daemon(self):
        while self.daemon_run:
            for i in range(0,20):
                sleep(1)
                if not self.daemon_run:
                    return
            for idx in range(len(self.connect_threads)-1,0,-1):
                if not self.connect_threads[idx].isAlive():
                    del self.connect_threads[idx]
            for idx in range(len(self.disconnect_threads)-1,0,-1):
                if not self.disconnect_threads[idx].isAlive():
                    del self.disconnect_threads[idx]

    def stopDaemon(self):
        self.daemon_run = False


    def addNode(self,ac):
        full_ac = self.access.addAccess(ac)
        if full_ac:
            node = Node()
            node.loadConfig(full_ac)
            node.connect()
            self.nodes.append(node)
            node.connect()
            return full_ac['id']
        else:
            return -1

    def delNode(self,nodeid):
        node = self.getNode(nodeid)
        if node:
            node.disconnect()
            self.nodes.remove(node)
            return self.access.delAccess(nodeid)
        else:
            return False

    def updateNode(self,nodeid,access_json):
        full_ac = self.access.updateAccess(nodeid, access_json)
        full_ac['id']=nodeid
        if full_ac:
            if isinstance(nodeid, unicode) or isinstance(nodeid, str):
                nodeid=int(nodeid)
            for index,node in enumerate(self.nodes):
                if node['id'] == nodeid:
                    node.disconnect()
                    node.loadConfig(full_ac)
                    node.connect()
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
            node = Node()
            node.loadConfig(nodeaccess)
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
                self.msg.put('mod', {'module': mod, 'result': res, 'nodeid': nodeid})
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
                    self.msg.put('mod', {'module': mod, 'result': res, 'nodeid': node['id']})
                th = threading.Thread(target = task)
                th.daemon = True
                th.start()
        return '{"id":"all", "msg":"Module `%s` executed on all nodes"}' % mod

