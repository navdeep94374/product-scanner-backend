from fastapi import HTTPException, status
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse
from bson.binary import Binary
from fastapi.encoders import jsonable_encoder
import uuid
from bson import ObjectId


def create_grocery_item(db,user,payload):
    try:
        #check if grocery list for that user already exist
        list_exist = db["groceries"].find_one({"user_id":str(user["_id"]),"_id":ObjectId(payload.list_id)})

        if not list_exist:
           return JSONResponse(status_code=404,content=ApiError("List not found", status_code=404, success=False).get_info())

        new_list_data = dict(payload).copy()
        new_list_data["user_id"] = str(user["_id"])
 
        inserted_result = db["groceries_items"].insert_one(new_list_data)
        created_list = db["groceries_items"].find_one({"_id":inserted_result.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED,content=ApiResponse("Grocery itesm added to list successfully",status_code=status.HTTP_201_CREATED,success=True,data=created_list).get_info())

    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())