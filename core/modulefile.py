#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os
import json

class ModuleFile:
    # STATUS:
    # 1: success
    # 0: fail

    def __init__(self):
        self.modulepath = os.path.join(os.getcwd(),'modules')

    def get(self):
        res=[]
        for desc in os.listdir(self.modulepath):
            if desc.endswith('.description'):
                with open(os.path.join(self.modulepath,desc)) as descf:
                    res_json = json.load(descf)
                    with open(os.path.join(self.modulepath,desc[:-12])) as modf:
                        res_json['content']=modf.read()
                        res.append(res_json)
        return json.dumps(res)

    def add(self, modulefilename, modulecontent,description_text='',default_argument=''):
        if modulefilename.endswith('.description'):
            return json.dumps({'status':0 ,'msg':'Module %s cannot end with ".description". Please change filename.' % modulefilename})
        mod = os.path.join(self.modulepath, modulefilename)
        desc = os.path.join(self.modulepath, modulefilename+'.description')
        if os.path.exists(mod) or os.path.exists(desc) :
            return json.dumps({'status':0 ,'msg':'Module %s Exists. Please change filename.' % modulefilename})
        else:
            with open(mod,'w') as modf:
                modf.write(modulecontent)
            with open(desc, 'w') as descf:
                json.dump({'module':modulefilename,'description':description_text,'argument':default_argument},descf,indent=2)
            return json.dumps({'status':1,'msg':"Module %s Added." % modulefilename})

    def delete(self, modulefilename):
        mod = os.path.join(self.modulepath, modulefilename)
        description = os.path.join(self.modulepath, modulefilename+'.description')
        if not os.path.exists(mod):
            return json.dumps({'status':0 ,'msg':'Module %s Not Exists' % modulefilename})
        else:
            os.remove(mod)
            os.remove(description)
            return json.dumps({'status':1,'msg':"Module %s Deleted." % modulefilename})
