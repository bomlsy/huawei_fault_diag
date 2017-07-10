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


# When a request is unprocessed, two types of text might be returned as HTML content:
# 1: None
# 2: not found
# please cover these situations in case any bug triggered.


urls = (
    '/', 'homepage',
    '/index.*', 'homepage',                      #### nodeid may be "all", param may be empty
    '/node/get/(.+)', 'node_get',                   # nodeid  (nodeid?detailed=1 will return detail)
    '/node/connect/(.+)','node_connect',            # nodeid
    '/node/disconnect/(.+)','node_disconnect',      # nodeid
    '/cmd/exec/(.+)/(.+)', 'cmd_exec',              # nodeid, cmdstr
    '/mod/exec/(.+)/(.+)/(.*)', 'mod_exec',         # nodeid, modname, param
    '/notification/get', 'notification_get',
)

class homepage:
    def GET(self):
        return web.seeother('/static/index.html')


class node_get:
    def GET(self, nodeid):
        req = web.input()
        if nodeid.isdigit():
            nodeid = int(nodeid)
            if req.has_key('detail'):
                return nodes.getDetailedStatus(nodeid)
            else:
                return nodes.getBasicStatus(nodeid)
        elif nodeid == "all":
            if req.has_key('detail'):
                return nodes.getAllDetailedStatus()
            else:
                return nodes.getAllBasicStatus()

class node_connect:
    def GET(self, nodeid):
        if nodeid.isdigit():
            return nodes.connectNode(int(nodeid))
        elif nodeid == "all":
            nodes.connectAllNodes()
            return '{"msg":"Disconnect Commands Sent"}'

class node_disconnect:
    def GET(self, nodeid):
        if nodeid.isdigit():
            return nodes.disconnectNode(int(nodeid))
        elif nodeid == "all":
            nodes.disconnectAllNodes()
            return '{"msg":"Disconnect Commands Sent"}'


class cmd_exec:
    def GET(self, nodeid, cmd):
        if nodeid.isdigit():
            nodeid = int(nodeid)
            return nodes.executeCmd(nodeid, cmd)
        elif nodeid == "all":
            return nodes.executeCmdAll(cmd)

class mod_exec:
    def GET(self, nodeid, mod, param):
        if nodeid.isdigit():
            nodeid = int(nodeid)
            return nodes.executeMod(nodeid, mod, param)
        elif nodeid == "all":
            return nodes.executeModAll(mod, param)

class notification_get:
    def GET(self):
        return nodes.getNotification()

nodes = Nodes()
nodes.loadNodeList('nodes.list')
nodes.connectAllNodes()

app = web.application(urls, globals())
webbrowser.open('http://127.0.0.1:'+str(default_listener_port),new=2)
app.run()
