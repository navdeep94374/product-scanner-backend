from fastapi import HTTPException, status
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse
from bson.binary import Binary
from fastapi.encoders import jsonable_encoder
import uuid
from bson import ObjectId


def delete_grocery_list(db,user,list_id):
    try:
        #check if grocery list for that user already exist
        list_exist = db["groceries"].find_one({"user_id":str(user["_id"]),"_id":ObjectId(list_id)})

        if not list_exist:
           return JSONResponse(status_code=404,content=ApiError("list not found", status_code=409, success=False).get_info())

        db["groceries"].delete_one({"_id":ObjectId(list_id)})
        db["groceries_items"].delete_many({"list_id":list_id})

        return JSONResponse(status_code=200,content=ApiResponse("Grocery list deleted successfully",status_code=200,success=True).get_info())

    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())