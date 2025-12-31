from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
import httpx

from ..database import SessionLocal
from .. import schemas
from .. import crud
from ..services.recipe_client import get_recipe
from ..utils.merge import merge_ingredients
from ..utils.auth import get_current_user_id
from ..metrics import shopping_carts_created


router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

EXAMPLE_CART = {
    "cart_id": 1,
    "user_id": 2,
    "name": "Weekly meals",
    "recipe_ids": [10, 11],
    "ingredients": [{"name": "tomato", "quantity": 2, "unit": "pcs"}],
    "created_at": "2025-01-01T12:00:00",
}

ERROR_401 = {
    "model": schemas.ErrorResponse,
    "description": "Unauthorized",
    "content": {"application/json": {"example": {"detail": "Invalid or expired token"}}},
}
ERROR_404 = {
    "model": schemas.ErrorResponse,
    "description": "Not found",
    "content": {"application/json": {"example": {"detail": "Cart not found"}}},
}
ERROR_500 = {
    "model": schemas.ErrorResponse,
    "description": "Internal error",
    "content": {"application/json": {"example": {"detail": "Internal server error"}}},
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
  

@router.post(
    "/",
    response_model=schemas.CartRead,
    summary="Create cart",
    responses={
        200: {"description": "OK", "content": {"application/json": {"example": EXAMPLE_CART}}},
        401: ERROR_401,
        422: {"description": "Validation error"},
        500: ERROR_500,
    },
)
async def create_cart(
    cart: schemas.CartCreate = Body(
        ...,
        examples={
            "example": {"value": {"name": "Weekly meals", "recipe_ids": [10, 11]}}
        },
    ),
    user_token = Depends(get_current_user_id),  
    db: Session = Depends(get_db),
):
    user_id, _ = user_token
    recipe_ids = cart.recipe_ids
    #if not recipe_ids:
    #    raise HTTPException(status_code=400, detail="No recipes provided")
    status = "success"
    try:
        ingredients = []
        for recipe_id in recipe_ids:
            recipe = await get_recipe(recipe_id)
            ingredients.extend(recipe["ingredients"])

        merged_ingredients = merge_ingredients(ingredients)

        created_cart = crud.create_shopping_cart(
            db=db,
            user_id=user_id,
            name=cart.name,
            recipe_ids=recipe_ids,
            ingredients=merged_ingredients,
        )
        shopping_carts_created.labels(source="api", status="success").inc()
        return created_cart
    except httpx.HTTPError:
        status = "error"
        raise
    except HTTPException:
        status = "error"
        raise
    except Exception as e:
        status = "error"
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shopping_carts_created.labels(source="api", status=status).inc()

@router.get(
    "/my",
    response_model=list[schemas.CartRead],
    summary="List my carts",
    responses={
        200: {"description": "OK", "content": {"application/json": {"example": [EXAMPLE_CART]}}},
        401: ERROR_401,
        422: {"description": "Validation error"},
        500: ERROR_500,
    },
)
def get_my_carts(
    user_token = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_id, _ = user_token
    carts = crud.get_all_carts_by_user(db, user_id)
    return carts

@router.get(
    "/{cart_id}",
    response_model=schemas.CartRead,
    summary="Get cart by id",
    responses={
        200: {"description": "OK", "content": {"application/json": {"example": EXAMPLE_CART}}},
        401: ERROR_401,
        404: ERROR_404,
        422: {"description": "Validation error"},
        500: ERROR_500,
    },
)
def get_cart(
    cart_id: int,
    user_token = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_id, _ = user_token
    cart = crud.get_cart(db, cart_id, user_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    return cart

@router.delete(
    "/{cart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete cart",
    responses={
        204: {"description": "Deleted"},
        401: ERROR_401,
        404: ERROR_404,
        422: {"description": "Validation error"},
        500: ERROR_500,
    },
)
def delete_cart(
    cart_id: int,
    user_token = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_id, _ = user_token
    result = crud.delete_cart(db, cart_id, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return None

@router.put(
    "/{cart_id}",
    response_model=schemas.CartRead,
    summary="Update cart",
    responses={
        200: {"description": "OK", "content": {"application/json": {"example": EXAMPLE_CART}}},
        401: ERROR_401,
        404: ERROR_404,
        422: {"description": "Validation error"},
        500: ERROR_500,
    },
)
async def update_cart(
    cart_id: int, 
    updates: schemas.CartUpdate,
    user_token = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_id, _ = user_token
    original_cart = crud.get_cart(db, cart_id, user_id) 
    if not original_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    new_ingredients = None

    if updates.recipe_ids is not None:
        ingredients = []
        for recipe_id in updates.recipe_ids:
            recipe = await get_recipe(recipe_id)
            for ingredient in recipe["ingredients"]:
                ingredients.append(ingredient)

        
        new_ingredients = merge_ingredients(ingredients)

    updated_cart = crud.update_shopping_cart(
        db=db,
        cart=original_cart,
        updates=updates,
        new_ingredients=new_ingredients
    )
    return updated_cart



