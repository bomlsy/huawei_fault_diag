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
                nodes.getDetailedStatus(nodeid)
            else:
                nodes.getBasicStatus(nodeid)
        else:
            if req.has_key('detail'):
                return nodes.getAllDetailedStatus()
            else:
                return nodes.getAllBasicStatus()


class connect_all:
    def GET(self):
        nodes.connectAllNodes()
        return '{"msg":"command sent"}'


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

app = web.application(urls, globals())
webbrowser.open('http://127.0.0.1:'+str(default_listener_port),new=2)
app.run()
