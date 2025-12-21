from app import crud, schemas


def test_crud_create_update_delete(db_session):
    cart = crud.create_shopping_cart(
        db=db_session,
        user_id=1,
        name="Weekly",
        recipe_ids=[1, 2],
        ingredients=[{"name": "milk", "quantity": 1, "unit": "l"}],
    )

    fetched = crud.get_cart(db_session, cart.cart_id, 1)
    assert fetched is not None
    assert fetched.name == "Weekly"

    updates = schemas.CartUpdate(name="Updated", recipe_ids=[3])
    updated = crud.update_shopping_cart(
        db=db_session,
        cart=cart,
        updates=updates,
        new_ingredients=[{"name": "eggs", "quantity": 2, "unit": "pcs"}],
    )

    assert updated.name == "Updated"
    assert updated.recipe_ids == [3]

    deleted = crud.delete_cart(db_session, cart.cart_id, 1)
    assert deleted is True
    assert crud.get_cart(db_session, cart.cart_id, 1) is None
