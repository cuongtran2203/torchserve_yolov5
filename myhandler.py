import logging
import onnxruntime
import torch 
import cv2 
import numpy as np
import torchvision
import torch 
import cv2 
import numpy as np
import torchvision
import time
from ts.torch_handler.base_handler import BaseHandler
from PIL import Image
import io
from process import *
from byte_tracker import BYTETracker

class MyHandler(BaseHandler):
    def __init__(self) :
        self._context=None
        self.initialized=False
        self.model='vehicle_v5n.onnx'
        self.providers = ['CPUExecutionProvider']
        self.data_meta=None
        self.img_data=None
        self.session = onnxruntime.InferenceSession(self.model, providers=self.providers)
        self.tracker=BYTETracker()
        self.test_size=(640,640)
    def initialize(self, context):
        self._context=context
        self.manifest=context.manifest
        properties=context.system_properties
        self.initialized=True
        
    def preprocess(self,data):
              
        image=data[0].get("data")
        
        if image is None:
            image= data[0].get("body")
        image = Image.open(io.BytesIO(image))
        
        img=np.array(image)
        self.img_data=img
        # image= np.frombuffer(image,dtype=np.int8)
        # image=np.array_equal(y.reshape)
        im = letterbox(img, 640, stride=32, auto=True)[0]
        im = im.transpose((2, 0, 1))[::-1]
        im = np.ascontiguousarray(im)
        im = torch.from_numpy(im)
        im = im.float()
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        return im
    def inference(self,blob):
        self.data_meta=blob
        outputs = self.session.run(None, {self.session.get_inputs()[0].name:np.asarray(blob)})
        # print("time :{:.3f} s".format(time.perf_counter()-start))
        output_data = torch.tensor(outputs[0])
        return output_data
    def postprocess(self,preds):
        res=[]
        y = non_max_suppression(preds, 0.25, 0.45)[0]
        y=np.array(y)
        height, width = self.img_data.shape[:2]
        filter_class = [0,1,2,3,4,5,6]
        bbox = scale_boxes(self.data_meta.shape[2:], y[:, :4], self.img_data.shape).round()
        if y is not None :
            online_targets = self.tracker.update(y, [height,width], self.test_size, filter_class)
            online_tlwhs = []
            online_ids = []
            online_scores = []
            cls=y[:,5]
            for t,box,cl in zip(online_targets,bbox,cls):
                tlwh = t.tlwh
                tid = t.track_id              
                online_tlwhs.append(tlwh)
                online_ids.append(tid)
                online_scores.append(t.score)      
                _box=list(map(int,box))
                
            res.append({"label":cls,"bbox":_box,"score":online_scores,"id online":online_ids})
        return [res]
    # def handle(self, data, context):
    #     if not self.initialized:
    #         self.initialized(context)
    #     model_input=self.preprocess(data)
    #     model_output=self.inference(model_input)
    #     return self.postprocess(model_output)
        