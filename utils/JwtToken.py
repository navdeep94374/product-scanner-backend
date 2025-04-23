from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi.responses import JSONResponse
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse
from fastapi import Depends,Request

ACCESS_TOKEN_EXPIRE_MINUTES = 24*60 
ALGORITHM = "HS256"
JWT_SECRET_KEY = "$2b$12$kB9GehVzEH18pSr.v6gCBeFuAd44S80sXI2uTohcKaNaZsqqXY2o6 "

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "/user/login")

def create_access_token(data:dict,exp:int = None):
    info = data.copy()
    if exp is not None:
        exp = datetime.utcnow() + timedelta(minutes=exp)
    else:
        exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    info.update({"exp":exp})
    return jwt.encode(info,JWT_SECRET_KEY,ALGORITHM)

def verify_access_token(token:str = Depends(oauth_scheme)):
    try:

        if not token:
            err = ApiError("failed to verify user",401,False).get_info()
            return JSONResponse(status_code=401,content=err)

        payload = jwt.decode(token,JWT_SECRET_KEY,ALGORITHM)
        email = payload.get("email")

        if email is None:
            err = ApiError("failed to verify user",401,False).get_info()
            return JSONResponse(status_code=401,content=err)
        
        return {"email":email}
    except Exception as e:
        err = ApiError("failed to verify user",401,False,str(e)).get_info()
        return JSONResponse(status_code=401,content=err)
    
def get_current_user(request:Request,token:str = Depends(oauth_scheme)):
    try:
        data = verify_access_token(token)
        user = request.app.database["users"].find_one({"email":data["email"]},{"password":0})

        if not user:
            err = ApiError("failed to verify user",401,False).get_info()
            return JSONResponse(status_code=401,content=err)

        return user
    except Exception as e:
        print(e)
        err = ApiError("failed to verify user",401,False,str(e)).get_info()
        return JSONResponse(status_code=401,content=err)


    

    
    