#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import signal
import sys
import webbrowser

import web

from core.history import History
from core.keyfile import KeyFile
from core.modulefile import ModuleFile
from core.nodes import *
from core.notification import Notification

from core.envsetup import setup_env

# When a request is unprocessed, two types of text might be returned as HTML content:
# 1: None
# 2: not found
# please cover these situations in case any bug triggered.


urls = (
    '/', 'homepage',
    '/index', 'homepage',
    '/index.*', 'homepage',                      #### nodeid may be "all", param may be empty
    '/node/get/(.+)', 'node_get',                   # nodeid  (nodeid?detail will return detail)
    '/node/connect/(.+)', 'node_connect',           # nodeid
    '/node/disconnect/(.+)', 'node_disconnect',     # nodeid
    '/node/add', 'node_add',                        # POST( access={"address":...} )
    '/node/delete/(.+)', 'node_delete',             # nodeid
    '/node/update/(.+)', 'node_update',             # nodeid, POST(new json access)
    '/module/get', 'module_get',
    '/module/add/(.*)', 'module_add',               # module name (empty for original name), POST(description,default_argument)
    '/module/delete/(.+)', 'module_delete',         # module name
    '/module/exec/(.+)/(.+)/(.*)', 'module_exec',   # nodeid, modname, param
    '/cmd/exec/(.+)/(.+)', 'cmd_exec',              # nodeid, cmdstr
    '/notification/get/(.+)', 'notification_get',
    '/key/get', 'key_get',
    '/key/add/(.*)', 'key_add',                     # keyname (empty for original name)
    '/key/delete/(.+)', 'key_delete',               # keyname
    '/history/add', 'history_add',
    '/history/save', 'history_save',                # POST history=textarea.value
    '/history/delete', 'history_delete',
)


class homepage:
    def GET(self):
        return web.seeother('/static/dashboard.html')


# Node

class node_get:
    def GET(self, nodeid):
        req = web.input()
        if nodeid.isdigit():
            nodeid = int(nodeid)
            if req.has_key('detail'):
                return nodes.getDetailStatus(nodeid)
            else:
                return nodes.getBasicStatus(nodeid)
        elif nodeid == "all":
            if req.has_key('detail'):
                return nodes.getAllDetailStatus()
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

class node_add:
    def POST(self):
        req = web.input()
        if req.has_key('access'):
            nodeid = nodes.addNode(req.get('access'))
            if nodeid >= 0:
                return '{"id": %d, "msg":"Node %d Added"}' % (nodeid,nodeid)
            else:
                return '{"msg":"Failed to add node"}'

class node_delete:
    def GET(self, nodeid):
        if nodeid.isdigit():
            nodeid = int(nodeid)
            if nodes.delNode(nodeid):
                return '{"id": %d, "msg":"Node %d Deleted"}' % (nodeid,nodeid)
            else:
                return '{"msg":"Failed to delete node"}'

class node_update:
    def POST(self,nodeid):
        if nodeid.isdigit():
            nodeid = int(nodeid)
            req = web.input()
            if req.has_key('access'):
                if nodes.updateNode(nodeid, req.get('access')):
                    return '{"id": %d, "msg":"Node %d Updated"}' % (nodeid,nodeid)
                else:
                    return '{"msg":"Failed to update node"}'

# Command

class cmd_exec:
    def GET(self, nodeid, cmd):
        if nodeid.isdigit():
            nodeid = int(nodeid)
            return nodes.executeCmd(nodeid, cmd)
        elif nodeid == "all":
            return nodes.executeCmdAll(cmd)

# Module

class module_get:
    def GET(self):
        return ModuleFile().get()

class module_add:
    def POST(self,modname):
        mf=web.input(myfile = {})
        if not mf.has_key('description'):
            desc = ''
        else:
            desc = mf['description']
        if not mf.has_key('default_argument'):
            arg = ''
        else:
            arg = mf['default_argument']
        if not modname:
            modname = mf['myfile'].filename
        return ModuleFile().add(modname, mf['myfile'].value, desc, arg)

class module_delete:
    def GET(self,modname):
        return ModuleFile().delete(modname)

class module_exec:
    def GET(self, nodeid, mod, param):
        if nodeid.isdigit():
            nodeid = int(nodeid)
            return nodes.executeMod(nodeid, mod, param)
        elif nodeid == "all":
            return nodes.executeModAll(mod, param)


# KEY

class key_get:
    def GET(self):
        return KeyFile().get()

class key_add:
    def POST(self,keyname):
        kf = web.input(myfile = {})
        if not keyname:
            keyname = kf['myfile']
        return KeyFile().add(keyname, kf['myfile'].value)

class key_delete:
    def GET(self,keyname):
        return KeyFile().delete(keyname)


# History

class history_get:
    def GET(self):
        return History().get()


class history_save:
    def POST(self):
        req = web.input()
        if req.has_key('history'):
            return History().save(req['history'])

class history_delete:
    def GET(self):
        return History().delete()


# Notification

class notification_get:
    def GET(self,event):
        return notification.get(event)



class EnhancedWebApp(web.application):
    def run(self,address="127.0.0.1", port=8080, *middleware):
        return web.httpserver.runsimple(self.wsgifunc(*middleware), (address, port))



setup_env()

# init a notification queue handler
notification = Notification()

# load Nodes and auto connect
nodes = Nodes()
nodes.loadAccess(access_file_name)
nodes.connectAllNodes()


# exit handler --
def exit_handler(signum,sock):
    print "Ctrl-C (%d) Captured. Disconnecting..." % signum
    nodes.access.stopdaemon()
    nodes.disconnectAllNodes()
    sleep(2)
    print "Server stopped."
    exit(0)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
# -- exit handler


# start web server
web.config.debug = False
app = EnhancedWebApp(urls, globals())
webbrowser.open('http://127.0.0.1:'+str(listen_port),new=2)
app.run(address = listen_address , port=listen_port)
