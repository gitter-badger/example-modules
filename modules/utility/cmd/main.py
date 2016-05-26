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
    cmd = params.CMD
    runcmd = 'cat'+' '+infile+'|'+'('+cmd+')'+'>'+outfile
    print('IN: {0}\nOUT: {1}\nCMD: {2}'.format(infile,
                                               outfile,
                                               cmd))
    print('RUNCMD: {0}'.format(runcmd))

    os.system(runcmd)
    
    print "Done"


if __name__ == "__main__":
    dc.run()
