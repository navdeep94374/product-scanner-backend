from fastapi import HTTPException, status
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse
from utils.HashPassword import HashPassword


def create_user(user, db):
    try:
        # Check if user already exists
        is_user_exist = db["users"].find_one({"email":user.email})

        if is_user_exist:
            info = ApiError("User  already exists", status_code=409, success=False).get_info()
            return JSONResponse(status_code=status.HTTP_409_CONFLICT,content=info)

        hashed_password = HashPassword.hashPwd(user.password)
        user_data = dict(user).copy()
        user_data["password"] = hashed_password
        user_data.pop("id")

        new_user = db["users"].insert_one(user_data)

        created_user = db["users"].find_one({"_id":new_user.inserted_id},{"password":0})

        return JSONResponse(status_code=status.HTTP_201_CREATED,content=ApiResponse("User created successfully",status_code=status.HTTP_201_CREATED,success=True,data=created_user).get_info())

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())