from fastapi import APIRouter,Depends,Request,Body
from utils.JwtToken import create_access_token, get_current_user
from schemas.user import ShowUser
from utils.ApiResponse import ApiResponse
from fastapi.responses import JSONResponse
from schemas.groceries import GroceriesList,GroceryItem
from repository.groceries.create_grocery_list import create_grocery_list
from repository.groceries.create_grocery_item import create_grocery_item
from repository.groceries.delete_grocery_list import delete_grocery_list
from repository.groceries.delete_grocery_item import delete_grocery_item
from repository.groceries.get_list_items import get_list_items

groceries_router = APIRouter(prefix="/groceries",tags=["groceries list"])



@groceries_router.get("/",status_code=200)
def get_list(request:Request,user:ShowUser=Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
    
    db = request.app.database
    grocery_list = db["groceries"].find()

    return JSONResponse(status_code=200,content=ApiResponse("list fetched successfully",status_code=200,success=True,data=list(grocery_list)).get_info())


@groceries_router.post("/",status_code=201)
def create_list(request:Request,payload:GroceriesList=Body(...),user:ShowUser=Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
    
    return create_grocery_list(request.app.database,user,payload)


@groceries_router.delete("/{list_id}",status_code=200)
def delete_list(request:Request,list_id:str,user:ShowUser=Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
    
    return delete_grocery_list(request.app.database,user,list_id)


@groceries_router.get("/{list_id}/items",status_code=200,tags=["groceries items"])
def get_items(request:Request,list_id:str,user:ShowUser=Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
    return get_list_items(request.app.database,user,list_id)

@groceries_router.post("/items",status_code=201,tags=["groceries items"])
def create_item(request:Request,payload:GroceryItem=Body(...),user:ShowUser=Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
    
    return create_grocery_item(request.app.database,user,payload)


@groceries_router.delete("/{list_id}/items/{item_id}",status_code=200,tags=["groceries items"])
def delete_item(request:Request,list_id:str,item_id:str,user:ShowUser=Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
    
    return delete_grocery_item(request.app.database,user,list_id,item_id)
