#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
import json
import os
import sys

def main():
    hr = HadoopRuntime("spec.json")
    settings = hr.settings
    print(settings)

    ds = json.load(open(settings.Input.DS))

    if ds['Type'] != "AWS S3":
        raise ValueError("Invalid data_source type: '%s'" % ds['Type'])

    # Prepare working directory
    hr.hdfs_clean_working_dir()
    output_dir = hr.get_hdfs_working_dir("sentiment_result")
    settings.Output.sentiment_result.val = output_dir

    # Execute "hadoop jar"
    jar_file = "HelloAvro-1.0-SNAPSHOT-jar-with-dependencies.jar"
    hadoop_params = {}
    hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params["AWS_ACCESS_KEY_ID"] = ds['Meta']['key']
    hadoop_params["AWS_SECRET_ACCESS_KEY"] = ds['Meta']['token']
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])
        
    jar_defs = {}
    jar_defs["mapreduce.framework.name"] = "yarn"
    jar_defs["yarn.resourcemanager.address"] = settings.Param.yarn_resourcemanager
    jar_defs["yarn.resourcemanager.scheduler.address"] = settings.Param.yarn_resourcemanager_scheduler
    jar_defs["fs.defaultFS"] = settings.Param.hdfs_root
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])
    
    cmd_str = '%s hadoop jar %s %s %s %s' % (hadoop_params_str, jar_file, jar_defs_str, ds['URL'], output_dir)
    print("Executing:")
    print(cmd_str)
    ret = os.system(cmd_str)
    sys.exit(ret)

if __name__ == "__main__":
    main()