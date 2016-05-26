#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)


import pandas as pd
import statsmodels.formula.api as smf


@dc.basic_runtime(spec_json="spec.json")
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here
    in_name = inputs.IN
    out_name = outputs.Results
    formula = params.Formula
    
    src_data = pd.read_csv(in_name, index_col=0)
    est = smf.ols(formula, data=src_data).fit()

    result = open(out_name, "w")
    result.write(est.summary().as_text())

    print "Done"


if __name__ == "__main__":
    dc.run()
