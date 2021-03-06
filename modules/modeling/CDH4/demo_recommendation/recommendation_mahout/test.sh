#!/bin/bash

set -x

# screwjack gen_ds \
#     --ds_type=s3 \
#     --ds_url=s3n://xiaolin/movielens/big/ratings.csv \
#     key=$AWS_ACCESS_KEY_ID \
#     token=$AWS_SECRET_ACCESS_KEY > input2.ds.json

# screwjack gen_ds \
#     --ds_type=http \
#     --ds_url=http://nlp.stanford.edu/courses/NAACL2013/NAACL2013-Socher-Manning-DeepLearning.pdf \
#     > input2.ds.json

screwjack gen_ds \
    --ds_type=hdfs \
    --ds_url=hdfs://10.10.0.162/tmp/movielens/big/ratings.csv \
    > ratings.ds.json

screwjack gen_ds \
    --ds_type=hdfs \
    --ds_url=hdfs://10.10.0.162/tmp/movielens/big/users.csv \
    > usersFile.ds.json

touch output.hdfs

screwjack run local \
    --param-hdfs_root="hdfs://10.10.0.162" \
    --param-AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
    --param-AWS_ACCESS_KEY_SECRET="$AWS_SECRET_ACCESS_KEY" \
    --param-yarn_resourcemanager="10.10.0.162:8032" \
    --param-yarn_resourcemanager_scheduler="10.10.0.162:8030" \
    --param-S3_BUCKET="xiaolin" \
    --ratings=ratings.ds.json \
    --usersFile=usersFile.ds.json \
    --output_path=output.hdfs && \
    cat output.hdfs

