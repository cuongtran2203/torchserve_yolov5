FROM pytorch/torchserve:latest
WORKDIR /
ADD requirements.txt myhandler.py results.py model-store service/
RUN pip3 install -r service/requirements.txt
RUN pip3 install onnx onnxruntime ts
CMD ["torchserve ","--start","--model-store service/model-store","--models Cuong2203=Cuong2203.mar","--ts-config service/config.properties"]

