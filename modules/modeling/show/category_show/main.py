#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)

import string
import pandas as pd
import matplotlib.pyplot as plt

@dc.basic_runtime(spec_json="spec.json")
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here
    in_filename = inputs.infile
    out_filename = outputs.outfile
    dlt = params.dlt
    col = int(string.atof(params.columns))
    df = pd.read_csv(in_filename, delimiter = dlt, header = None)

    res = {}
    for i in df[col]:
        res[i] = res.get(i, 0) + 1
    category_list = res.keys()
    category_cnt = res.values()

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)
    ax.pie(category_cnt, labels = category_list, autopct = '%3.1f%%', startangle = 90)
    fig.savefig(out_filename, format = "png")
    
    print "Done"


if __name__ == "__main__":
    dc.run()
