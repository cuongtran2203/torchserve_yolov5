FROM python:3.8.16-bullseye

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y openjdk-11-jre && apt-get clean 

RUN useradd -m model-server

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD start.sh config.properties  service/
ADD model-store service/model-store/

WORKDIR /service/
RUN chmod +x /service/start.sh \
    && chown -R model-server /service
RUN chown -R model-server /service/model-store
USER model-server

ENTRYPOINT [ "/service/start.sh"  ]
CMD [ "serve" ]
