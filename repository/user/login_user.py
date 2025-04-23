
from fastapi.responses import JSONResponse
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi import status
from utils.JwtToken import create_access_token
from utils.HashPassword import HashPassword


def login_user(request,db):
    try:
        is_user_exist = db["users"].find_one({"email":request.username})


        if not is_user_exist:
            info = ApiError("User not found", status_code=status.HTTP_404_NOT_FOUND, success=False).get_info()
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=info)
        
        password = is_user_exist["password"]

        if not HashPassword.verifyPwd(request.password,password):
            info = ApiError("Invalid login credentials", status_code=status.HTTP_401_UNAUTHORIZED, success=False).get_info()
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content=info)


        email = is_user_exist["email"]
        token = create_access_token({"email":email})
        
        return {"access_token":token,"token_type":"bearer"}
        # return ApiResponse("login success",status_code=status.HTTP_200_OK,success=True,data={"access_token":token,"token_type":"bearer"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())

 