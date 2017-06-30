#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import ConfigParser

global_config_file_name = 'global.ini'
global_config = ConfigParser.ConfigParser()
global_config.read('config/' + global_config_file_name)

default_port = int(global_config.get('access', 'default_port', 22))
default_username = global_config.get('access', 'default_username', 'root')
default_password = global_config.get('access', 'default_password', '')
default_authtype = global_config.get('access', 'default_authtype', 'password')
default_key = global_config.get('access', 'default_key', '')
