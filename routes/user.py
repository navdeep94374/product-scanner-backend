from fastapi import APIRouter,Depends,Request,Body
from fastapi.security import OAuth2PasswordRequestForm
from repository.user.update_user import update_user
from schemas.user import UpdateUser, User,ShowUser
from repository.user.create_user import create_user
from repository.user.login_user import login_user
from utils.JwtToken import create_access_token, get_current_user
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse

user_router = APIRouter(prefix="/user",tags=["auth"])

@user_router.post("/signup",status_code=201,response_model=None)
def signup(request:Request,user:User=Body(...)):
    return create_user(user,request.app.database)

@user_router.post("/login",status_code=200)
def login(request:Request,form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data,request.app.database)

@user_router.put("/update",status_code=200)
def update(request:Request,payload:UpdateUser=Body(...),user:ShowUser = Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user

    return update_user(payload,request.app.database,user)

@user_router.get("/me")
def me(refresh_at:bool = False,user = Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user

    user_info = dict(user).copy()
    user_info["access_token"] = None

    if refresh_at:
        token = create_access_token({"email":user["email"]})
        user_info["access_token"] = token

    return JSONResponse(status_code=200,content=ApiResponse("User fetched successfully",200,True,data=user_info).get_info())
