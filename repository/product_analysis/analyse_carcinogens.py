from fastapi.responses import JSONResponse
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse , clean_text
from fastapi import status
import PIL
from PIL import Image, ImageOps
import numpy as np
import easyocr
import re
from carcinogens_model.detect_carcinogens import check_carcinogen


ocr = easyocr.Reader(["en"])

def analyse_carcinogens(db,user,image):
    try:

        if not image:
            JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Image is required for analyyis", status_code=422, success=False).get_info())

        imgFile = np.array(PIL.Image.open(image.file).convert("RGB"))
        results = ocr.readtext(imgFile)
        text = " ".join([clean_text(res[1]) for res in results])
        res = check_carcinogen(text)

        return JSONResponse(status_code=200,content=ApiResponse("Carciongens analysis sucess",200,True,{"carcinogens":res}).get_info())


    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())