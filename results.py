from myhandler import MyHandler
_service=MyHandler()
def handle(data,context):
    if data is None :
        return None 
    data=_service.preprocess(data)
    data=_service.inference(data)
    data=_service.postprocess(data)
    return data