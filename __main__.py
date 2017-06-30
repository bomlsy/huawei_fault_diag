#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import modules.controller
import web
from modules.controller import *
import time, random

urls = (
    '/connect_all', 'connect_all',
    '/getnodes', 'getnodes',
    '/exec', 'execute'
)


class getnodes:
    def GET(self):
        return nodes.getAllDetailedStatus()


class connect_all:
    def GET(self):
        nodes.connectAllNodes()
        return '{"msg":"command sent"}'


class execute:
    def GET(self):
        req = web.input()
        if req.has_key('cmd') and req.has_key('node'):
            cmd = req.get('cmd')
            nodeid = int(req.get('node'))
            return nodes.executeCmd(cmd, nodeid)


nodes = Nodes()
nodes.loadNodeList('nodes.list')

app = web.application(urls, globals())
app.run()
