#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import genfromtxt
from sklearn import preprocessing

from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)


@dc.basic_runtime(spec_json="spec.json")
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here
    in_name = inputs.IN
    out_name = outputs.OUT
    src_data = np.genfromtxt(in_name, delimiter=",")
    scaler = preprocessing.StandardScaler()
    scaler.fit(src_data)
    standdata = scaler.transform(src_data)
    np.savetxt(out_name, standdata, delimiter=",")
    
    print "Done"


if __name__ == "__main__":
    dc.run()
