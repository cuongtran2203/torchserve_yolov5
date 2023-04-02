
# Transform the input image into a bytes object
import cv2
from PIL import Image
from io import BytesIO
import grpc
import inference_pb2
import inference_pb2_grpc
import management_pb2_grpc
import requests
import time 
import numpy as np
def infer(stub, model_name, model_input):
    request=stub.Predictions(
        inference_pb2.PredictionsRequest(
            model_name = model_name,
            input = {'data': model_input}
        )
    )
    return request
if __name__ == '__main__':
    channel=grpc.insecure_channel('localhost:7070')
    stub = inference_pb2_grpc.InferenceAPIsServiceStub(channel)
    filename="image.jpg"
    image = Image.fromarray(cv2.imread(filename))
    image2bytes = BytesIO()
    image.save(image2bytes, format="JPEG")
    image2bytes.seek(0)
    image_as_bytes = image2bytes.read()

    # Send the HTTP POST request to TorchServe
    times=[]
    count=0
    for i in range(10):
        time_start=time.time()
        # req = requests.post("http://localhost:8080/predictions/VehicleDetection", data=image_as_bytes)
        # if count%5000==0:
        #     rep1=requests.post("http://localhost:8080/predictions/LaneDetection", data=image_as_bytes)
        #     count+=1
        response = infer(stub, 'VehicleDetection', image_as_bytes)
        print(response)
            
        # if req.status_code == 200: 
        #     res = req.json()
        #     res2=rep1.json()
        #     print(res)
        #     print(res2)
        took = time.time() -time_start
        times.append(took)
        print(f'Took \t: {took}')
    times = np.array(times)
    print(f'Mean time \t: {np.mean(times)}')
    print(f'Median time \t: {np.median(times)}')
    
