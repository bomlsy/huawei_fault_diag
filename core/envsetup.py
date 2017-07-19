#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import sys,os,signal
from time import sleep

if __name__ == "__main__":
    exit(0)



def setup_env():

    # ensure current directory
    os.chdir(sys.path[0])
    # mkdir

    def ensureDirExists(path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
                os.mkdir(path)
        else:
            os.mkdir(path)
        # remove .gitkeep
        if os.path.exists(os.path.join(path, '.gitkeep')):
            os.remove(os.path.join(path, '.gitkeep'))


    ensureDirExists('cache')
    ensureDirExists('config')
    ensureDirExists(os.path.join('config','keyfile'))
    ensureDirExists('modules')
