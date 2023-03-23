FROM python:3.8.16-bullseye


# setup python

ADD requirements.txt myhandler.py results.py start.sh config.properties  service/
ADD model-store service/model-store/
RUN apt update & apt upgrade -y
RUN pip install -r service/requirements.txt
RUN apt install default-jdk
RUN apt install nano 
RUN update-alternatives --config java
RUN export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

CMD ["sh","service/start.sh"]