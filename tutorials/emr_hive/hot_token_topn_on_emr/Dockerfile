# hot_token_topN_on_emr

# VERSION : 0.1

FROM zetdata/ubuntu:trusty
# MAINTAINER Your_name, Your_email_address

RUN pip install boto

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD main.hql /home/run/
ADD resources /home/run/resources/