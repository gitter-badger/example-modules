#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


@dc.basic_runtime(spec_json="spec.json")
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here
    in_name = inputs.IN
    out_name1 = outputs.Residuals_1
    out_name2 = outputs.Residuals_2
    out_name3 = outputs.Coefficient
    
    data = np.genfromtxt(in_name, delimiter=",")
    info = data[:,0:-1]
    target = data[:,-1]
    
    lr = LinearRegression()
    lr.fit(info, target)
    predicted = lr.predict(info)

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)
    ax.hist(predicted - target, bins=50, label="Residuals Linear", alpha=.5);
    ax.set_title("Histogram of Residuals")
    ax.legend(loc="best")
    fig.savefig(out_name1, format = "png")
    

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)
    ax.scatter(target, predicted)
    ax.plot([target.min(), target.max()], [target.min(), target.max()], "k--", lw=5)
    ax.set_xlabel("Measured")
    ax.set_ylabel("Predicted")
    fig.savefig(out_name2, format = "png")

    np.savetxt(out_name3, lr.coef_, delimiter=",")

    print "Done"


if __name__ == "__main__":
    dc.run()
