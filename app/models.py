from sqlalchemy import Column, Integer, TIMESTAMP, JSON, String
from .database import Base
from sqlalchemy.sql import func



class ShoppingCart(Base):
    __tablename__ = "shopping_carts"
    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    recipe_ids = Column(JSON, nullable=True)
    name = Column(String, nullable=False)
    ingredients = Column(JSON, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
