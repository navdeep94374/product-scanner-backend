from fastapi import APIRouter,Depends,Body,Request,File, UploadFile
from repository.product_analysis.analyse_product import analyse_product
from utils.JwtToken import get_current_user
from pydantic import BaseModel
from repository.product_analysis.analyse_carcinogens import analyse_carcinogens

class ProductAnalysisReq(BaseModel):
    product_code:str


product_analysis_router = APIRouter(prefix="/analysis",tags=["product_analysis"])

@product_analysis_router.post("/",status_code=201)
def analyse(request:Request,payload:ProductAnalysisReq = Body(...),user = Depends(get_current_user)):
    # unauthenticated user
    if not isinstance(user, dict):
        return user
        
    return analyse_product(request.app.database,user,payload)

@product_analysis_router.post("/carcinogens",status_code=201)
def detect_carcinogens(request:Request,image: UploadFile = File(...)):
     # unauthenticated user
    user = {"email":"Aa"}
    if not isinstance(user, dict):
        return user
    
    return analyse_carcinogens(request.app.database,user,image)
