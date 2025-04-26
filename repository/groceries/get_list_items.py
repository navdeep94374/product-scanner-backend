from fastapi import HTTPException, status
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse
from bson.binary import Binary
from fastapi.encoders import jsonable_encoder
import uuid
from bson import ObjectId


def get_list_items(db,user,list_id):
    try:
        #check if grocery list for that user already exist
        grocery_list = db["groceries"].find_one({"_id":ObjectId(list_id)})

        if not grocery_list:
           return JSONResponse(status_code=404,content=ApiError("list not found", status_code=409, success=False).get_info())

        items = db["groceries_items"].find({"list_id":list_id})
   
        return JSONResponse(status_code=200,content=ApiResponse("Items fetched successfully",status_code=200,success=True,data=list(items)).get_info())

    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())