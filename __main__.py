#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import web,sys
import webbrowser
from core.controller import *

# set port
if sys.argv.__len__() > 1:
    sys.argv[1] = str(default_listener_port)
else:
    sys.argv.append(str(default_listener_port))

urls = (
    '/','homepage',
    '/connect_all', 'connect_all',
    '/disconnect_all', 'disconnect_all',
    '/connect','connect',
    '/disconnect','disconnect',
    '/getnodes', 'getnodes',
    '/exec_cmd', 'exec_cmd',
    '/exec_mod', 'exec_mod',
    '/getnotification', 'getnotification'
)


class homepage:
    def GET(self):
        return web.seeother('/static/index.html')


class getnodes:
    def GET(self):
        req = web.input()
        if req.has_key('node'):
            nodeid = int(req.get('node'))
            if req.has_key('detail'):
                return nodes.getDetailedStatus(nodeid)
            else:
                return nodes.getBasicStatus(nodeid)
        else:
            if req.has_key('detail'):
                return nodes.getAllDetailedStatus()
            else:
                return nodes.getAllBasicStatus()


class connect_all:
    def GET(self):
        nodes.connectAllNodes()
        return '{"msg":"Connect Commands Sent"}'

class disconnect_all:
    def GET(self):
        nodes.disconnectAllNodes()
        return '{"msg":"Disconnect Commands Sent"}'

class connect:
    def GET(self):
        req = web.input()
        if req.has_key('node'):
            nodeid = req.get('node')
            return nodes.connectNode(nodeid)
        else:
            return '{"msg":"ERROR: No node specified to connect"}'

class disconnect:
    def GET(self):
        req = web.input()
        if req.has_key('node'):
            nodeid = req.get('node')
            return nodes.disconnectNode(nodeid)
        else:
            return '{"msg":"ERROR: No node specified to disconnect"}'


class exec_cmd:
    def GET(self):
        req = web.input()
        if req.has_key('cmd'):
            cmd = req.get('cmd')
            if req.has_key('node'):
                nodeid = int(req.get('node'))
                return nodes.executeCmd(nodeid , cmd)
            else:
                return nodes.executeCmdAll(cmd)
    def POST(self):
        return self.GET()

class exec_mod:
    def GET(self):
        req = web.input()
        if req.has_key('mod'):
            mod = req.get('mod')
            if req.has_key('param'):
                param=req.get('param')
            else:
                param=''
            if req.has_key('node'):
                nodeid = int(req.get('node'))
                return nodes.executeMod(nodeid , mod, param)
            else:
                return nodes.executeModAll(mod, param)
    def POST(self):
        return self.GET()


class getnotification:
    def GET(self):
        return nodes.getNotification()

nodes = Nodes()
nodes.loadNodeList('nodes.list')
nodes.connectAllNodes()

app = web.application(urls, globals())
webbrowser.open('http://127.0.0.1:'+str(default_listener_port),new=2)
app.run()
