#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import ConfigParser

global_config_file_name = 'global.ini'
global_config = ConfigParser.ConfigParser()
global_config.read('config/' + global_config_file_name)


# backend
listen_port = int(global_config.get('backend', 'listen_port', 8080))
listen_address = global_config.get('backend', 'listen_address', '127.0.0.1')

# access
access_file_name = global_config.get('access', 'access_file_name', 'nodes.list')
default_port = int(global_config.get('access', 'default_port', 22))
default_username = global_config.get('access', 'default_username', 'root')
default_password = global_config.get('access', 'default_password', '')
default_authtype = global_config.get('access', 'default_authtype', 'password')
default_key = global_config.get('access', 'default_key', '')
tcp_connect_timeout = float(global_config.get('access', 'tcp_connect_timeout', 5))
command_timeout = float(global_config.get('access', 'command_timeout', 10))
