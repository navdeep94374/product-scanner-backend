
from fastapi.responses import JSONResponse
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi import status
from utils.JwtToken import create_access_token
from utils.HashPassword import HashPassword


def update_user(payload,db,user):
    try:
        user = db["users"].find_one({"email":user["email"]})

        if not user:
            info = ApiError("User not found", status_code=status.HTTP_404_NOT_FOUND, success=False).get_info()
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=info)
        
        update_fields = {k: v for k, v in payload.dict(exclude_unset=True).items()}
    
        if not update_fields:
            info = ApiError("No fields to update", status_code=status.HTTP_404_NOT_FOUND, success=False).get_info()
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=info)

        result = db["users"].update_one({"email":user["email"]},{"$set":update_fields})

        updated_user = db["users"].find_one({"email":user["email"]},{"password":0})  
        return JSONResponse(status_code=status.HTTP_200_OK,content=ApiResponse("User updated successfully",status_code=status.HTTP_200_OK,success=True,data=updated_user).get_info())
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())
 