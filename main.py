from fastapi import FastAPI,Depends, Request
from routes.user import user_router
from routes.analysis import product_analysis_router
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

env_config = dotenv_values(".env")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(env_config["MONGODB_CONNECTION_URL"])
    app.database = app.mongodb_client[env_config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    # app.database = {"db":"aa"}

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user_router)
app.include_router(product_analysis_router)
