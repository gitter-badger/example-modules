#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)

import os

@dc.basic_runtime(spec_json="spec.json")
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here

    infile = inputs.IN
    outfile = outputs.OUT
    plugin = inputs.PLUGIN
    chmod = 'chmod u+x'+' '+plugin
    runcmd = 'cat'+' '+infile+'|'+plugin+'>'+outfile
    print('IN: {0}\nOUT: {1}\nPLUGIN: {2}'.format(infile,
                                                      outfile,
                                                      plugin))
    print('chmod: {0}'.format(chmod))
    print('RUNCMD: {0}'.format(runcmd))

    os.system(chmod)
    os.system(runcmd)
    
    print "Done"


if __name__ == "__main__":
    dc.run()
