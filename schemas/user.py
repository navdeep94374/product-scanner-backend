from pydantic import BaseModel,Field
import uuid
from typing import Optional,List
from enum import Enum

class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"
    not_disclosed = "Not Disclosed"

class User(BaseModel):
    id:Optional[str] = Field(default_factory=uuid.uuid4,alias="_id")
    name:str
    email:str
    password:str
    weight:Optional[float] = None
    height:Optional[float] = None
    age:Optional[int] = None
    gender:Optional[Gender] = Gender["not_disclosed"].value
    allergen_info:Optional[List[str]] = []
    ingredient_pref:Optional[List[str]] = None

class ShowUser(BaseModel):
    email:str
    name:str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    allergen_info: Optional[List[str]] = None
    ingredient_pref:Optional[List[str]] = None
