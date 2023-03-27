
# Transform the input image into a bytes object
import cv2
from PIL import Image
from io import BytesIO
filename="image.jpg"
image = Image.fromarray(cv2.imread(filename))
image2bytes = BytesIO()
image.save(image2bytes, format="PNG")
image2bytes.seek(0)
image_as_bytes = image2bytes.read()

# Send the HTTP POST request to TorchServe
import requests
import time 
time_start=time.perf_counter()
req = requests.post("http://localhost:8080/predictions/Cuong2203", data=image_as_bytes)
print("time response :",time.perf_counter()-time_start)
if req.status_code == 200: 
    res = req.json()
    print(res)
