#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import signal
import web,sys,os
import webbrowser
from core.nodes import *
from core.notification import Notification
from core.keyfile import KeyFile
from core.modulefile import ModuleFile

# When a request is unprocessed, two types of text might be returned as HTML content:
# 1: None
# 2: not found
# please cover these situations in case any bug triggered.


urls = (
    '/', 'homepage',
    '/index.*', 'homepage',                      #### nodeid may be "all", param may be empty
    '/node/get/(.+)', 'node_get',                   # nodeid  (nodeid?detailed will return detail)
    '/node/connect/(.+)', 'node_connect',           # nodeid
    '/node/disconnect/(.+)', 'node_disconnect',     # nodeid
    '/node/add', 'node_add',                        # POST( access={"address":...} )
    '/node/delete/(.+)', 'node_delete',             # nodeid
    '/node/update/(.+)', 'node_update',             # nodeid, POST(new json access)
    '/module/get', 'module_get',
    '/module/add/(.*)', 'module_add',               # module name (empty for original name), POST(description,default_argument)
    '/module/del/(.+)', 'module_del',               # module name
    '/module/exec/(.+)/(.+)/(.*)', 'module_exec',   # nodeid, modname, param
    '/cmd/exec/(.+)/(.+)', 'cmd_exec',              # nodeid, cmdstr
    '/notification/get', 'notification_get',
    '/key/get', 'key_get',
    '/key/add/(.*)', 'key_add',                     # keyname (empty for original name)
    '/key/del/(.+)', 'key_del',                     # keyname
)


class homepage:
    def GET(self):
        return web.seeother('/static/index.html')


# Node

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
        return ModuleFile().getModules()

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
        return ModuleFile().addModule(modname, mf['myfile'].value, desc, arg)

class module_del:
    def GET(self,modname):
        return ModuleFile().delModule(modname)

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
        return KeyFile().getKeys()

class key_add:
    def POST(self,keyname):
        kf = web.input(myfile = {})
        if not keyname:
            keyname = kf['myfile']
        return KeyFile().addKey(keyname, kf['myfile'].value)

class key_del:
    def GET(self,keyname):
        return KeyFile().delKey(keyname)


# Notification

class notification_get:
    def GET(self):
        return notification.get()





class EnhancedWebApp(web.application):
    def run(self,address="127.0.0.1", port=8080, *middleware):
        return web.httpserver.runsimple(self.wsgifunc(*middleware), (address, port))


def exit_handler(signum,frame):
    print "Ctrl-C (%d) Captured. Exiting." % signum
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    # ensure current directory
    os.chdir(sys.path[0])


    # init a notification queue handler
    notification = Notification()

    # load Nodes and auto connect
    nodes = Nodes()
    nodes.loadAccess('nodes.list')
    nodes.connectAllNodes()

    # start web server
    web.config.debug = False
    app = EnhancedWebApp(urls, globals())
    #webbrowser.open('http://127.0.0.1:'+str(default_listener_port),new=2)
    app.run(port=default_listener_port)
