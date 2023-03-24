FROM python:3.8.16-bullseye


# setup python

ADD requirements.txt myhandler.py results.py start.sh config.properties  service/
ADD model-store service/model-store/
RUN apt update & apt upgrade -y
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN pip install -r service/requirements.txt
RUN apt-get update
RUN apt-get install -y openjdk-11-jre && apt-get clean 
WORKDIR /service/

RUN useradd -m model-server
RUN chmod +x /service/start.sh \
    && chown -R model-server /service
RUN chown -R model-server /service/model-store
USER model-server

ENTRYPOINT [ "/service/start.sh"  ]
CMD [ "serve" ]
