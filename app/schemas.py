from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartIngredient(BaseModel):
    name: str
    quantity: float
    unit: str

class CartCreate(BaseModel):
    name: str
    recipe_ids: Optional[List[int]] = []

class CartRead(BaseModel):
    cart_id: int
    user_id: int
    name: str
    recipe_ids: Optional[List[int]] = []
    ingredients: List[CartIngredient]
    created_at: datetime

    class Config:
        orm_mode = True

class CartUpdate(BaseModel):
    name: Optional[str] = None
    recipe_ids: Optional[List[int]] = None 


class ErrorResponse(BaseModel):
    detail: str


class RootResponse(BaseModel):
    msg: str


class HealthResponse(BaseModel):
    status: str
