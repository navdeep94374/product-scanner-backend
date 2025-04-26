from pydantic import BaseModel,Field
import uuid
from typing import Optional,List
from enum import Enum
from datetime import datetime

class GroceryItem(BaseModel):
    list_id:str
    name:str
    qty:int
    notes:Optional[str] = None
    isBought:bool = False
    category:Optional[str] = "Default"
    created_at: datetime = Field(default_factory=datetime.utcnow().isoformat)
    updated_at: datetime = Field(default_factory=datetime.utcnow().isoformat)


class GroceriesList(BaseModel):
    name : str
    user_id:str
    created_at: datetime = Field(default_factory=datetime.utcnow().isoformat)
    updated_at: datetime = Field(default_factory=datetime.utcnow().isoformat)


class InsertGroceryItem(BaseModel):
    list_id:str
    items : List[GroceryItem]
    