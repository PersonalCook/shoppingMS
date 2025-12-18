from sqlalchemy.orm import Session
from . import models, schemas


def create_shopping_cart(db:Session, user_id:int, name: str, recipe_ids: list, ingredients: list):

    db_cart = models.ShoppingCart(
        user_id=user_id,
        name=name,
        recipe_ids=recipe_ids,
        ingredients=ingredients
    )

    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


def get_shopping_cart(db:Session, cart_id:int):
    cart = db.query(models.ShoppingCart).filter(models.ShoppingCart.cart_id == cart_id).first()

    return cart if cart else None

def get_cart(db: Session, cart_id: int, user_id: int):

    return db.query(models.ShoppingCart).filter(
        models.ShoppingCart.cart_id == cart_id,
        models.ShoppingCart.user_id == user_id
    ).first()


def get_all_carts_by_user(db:Session, user_id:int):
    carts = db.query(models.ShoppingCart).filter(models.ShoppingCart.user_id == user_id).all()

    return carts

def delete_cart(db: Session, cart_id: int, user_id: int):

    cart = db.query(models.ShoppingCart).filter(
        models.ShoppingCart.cart_id == cart_id,
        models.ShoppingCart.user_id == user_id
    ).first()

    if not cart:
        return None

    db.delete(cart)
    db.commit()
    return True

def update_shopping_cart(db: Session, cart: models.ShoppingCart, updates: schemas.CartUpdate, new_ingredients: list):

    if updates.name is not None:
        cart.name = updates.name

    if updates.recipe_ids is not None:
        cart.recipe_ids = updates.recipe_ids
        cart.ingredients = new_ingredients

    db.commit()
    db.refresh(cart)
    return cart