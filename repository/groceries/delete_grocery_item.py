from fastapi import HTTPException, status
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse
from bson.binary import Binary
from fastapi.encoders import jsonable_encoder
import uuid
from bson import ObjectId


def delete_grocery_item(db,user,list_id,item_id):
    try:
        #check if grocery list for that user already exist
        item = db["groceries_items"].find_one({"list_id":list_id,"_id":ObjectId(item_id)})

        if not item:
           return JSONResponse(status_code=404,content=ApiError("item not found", status_code=409, success=False).get_info())

        db["groceries_items"].delete_one({"_id":ObjectId(item_id)})

        return JSONResponse(status_code=200,content=ApiResponse("Item removed successfully",status_code=200,success=True).get_info())

    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())