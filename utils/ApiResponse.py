
from bson import ObjectId


def serialize_objectid(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {key: serialize_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_objectid(item) for item in data]
    return data


def clean_text(text):
    import re
    text = text.lower()
    text = re.sub(r'\\x[0-9a-fA-F]{2}', '', text)
    text = re.sub(r'[\n\r\t]+', ' ', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = text.strip()
    return text

class ApiResponse:
    def __init__(self,msg,status_code,success,data=None):
        self.info = {"msg":msg,"status_code":status_code,"success":success,"data":serialize_objectid(data)}
    
    def get_info(self):
        return self.info



