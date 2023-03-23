FROM python:3.8.16-bullseye


# setup python

ADD requirements.txt myhandler.py results.py start.sh config.properties model-store service/
RUN apt update & apt upgrade -y
RUN pip install -r service/requirements.txt
RUN pip install onnx onnxruntime ts

CMD ["sh","service/start.sh"]