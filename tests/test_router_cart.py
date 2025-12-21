import os

import httpx
import jwt

from app import crud
from app.routers import shopping


def _auth_headers(user_id=1):
    token = jwt.encode(
        {"user_id": user_id},
        os.environ["JWT_SECRET"],
        algorithm=os.environ["JWT_ALGORITHM"],
    )
    return {"Authorization": f"Bearer {token}"}


def test_create_cart_merges_ingredients(client, db_session, monkeypatch):
    async def fake_get_recipe(recipe_id):
        if recipe_id == 1:
            return {"ingredients": [{"name": "milk", "unit": "l", "quantity": 1}]}
        return {
            "ingredients": [
                {"name": "milk", "unit": "l", "quantity": 0.5},
                {"name": "flour", "unit": "g", "quantity": 200},
            ]
        }

    monkeypatch.setattr(shopping, "get_recipe", fake_get_recipe)

    response = client.post(
        "/cart/",
        json={"name": "Weekly", "recipe_ids": [1, 2]},
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    merged = {(item["name"], item["unit"]): item["quantity"] for item in body["ingredients"]}
    assert body["name"] == "Weekly"
    assert body["user_id"] == 1
    assert merged[("milk", "l")] == 1.5


def test_get_my_carts_filters_by_user(client, db_session):
    crud.create_shopping_cart(
        db=db_session,
        user_id=1,
        name="Mine",
        recipe_ids=[1],
        ingredients=[{"name": "milk", "quantity": 1, "unit": "l"}],
    )
    crud.create_shopping_cart(
        db=db_session,
        user_id=2,
        name="Other",
        recipe_ids=[2],
        ingredients=[{"name": "flour", "quantity": 100, "unit": "g"}],
    )

    response = client.get("/cart/my", headers=_auth_headers(1))
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mine"


def test_get_cart_not_found(client, db_session):
    response = client.get("/cart/999", headers=_auth_headers())
    assert response.status_code == 404


def test_delete_cart_not_found(client, db_session):
    response = client.delete("/cart/999", headers=_auth_headers())
    assert response.status_code == 404


def test_update_cart_refreshes_ingredients(client, db_session, monkeypatch):
    async def fake_get_recipe(recipe_id):
        return {"ingredients": [{"name": "eggs", "unit": "pcs", "quantity": 2}]}

    monkeypatch.setattr(shopping, "get_recipe", fake_get_recipe)

    cart = crud.create_shopping_cart(
        db=db_session,
        user_id=1,
        name="Initial",
        recipe_ids=[1],
        ingredients=[{"name": "milk", "quantity": 1, "unit": "l"}],
    )

    response = client.put(
        f"/cart/{cart.cart_id}",
        json={"name": "Updated", "recipe_ids": [3]},
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Updated"
    assert body["ingredients"][0]["name"] == "eggs"


def test_recipe_service_failure_returns_500(client, db_session, monkeypatch):
    async def fake_get_recipe(recipe_id):
        raise httpx.HTTPError("Recipe service down")

    monkeypatch.setattr(shopping, "get_recipe", fake_get_recipe)

    response = client.post(
        "/cart/",
        json={"name": "Weekly", "recipe_ids": [1]},
        headers=_auth_headers(),
    )

    assert response.status_code == 500


def test_missing_auth_returns_403(client, db_session):
    response = client.get("/cart/my")
    assert response.status_code == 403


def test_invalid_auth_returns_401(client, db_session):
    token = jwt.encode(
        {"user_id": 1},
        "wrong-secret",
        algorithm=os.environ["JWT_ALGORITHM"],
    )
    response = client.get("/cart/my", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
