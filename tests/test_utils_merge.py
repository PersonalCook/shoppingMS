from app.utils.merge import merge_ingredients


def test_merge_ingredients_combines_quantities():
    ingredients = [
        {"name": "milk", "unit": "l", "quantity": 1},
        {"name": "milk", "unit": "l", "amount": 0.5},
        {"name": "flour", "unit": "g", "quantity": "200"},
    ]

    result = merge_ingredients(ingredients)
    result_by_key = {(item["name"], item["unit"]): item["quantity"] for item in result}

    assert result_by_key[("milk", "l")] == 1.5
    assert result_by_key[("flour", "g")] == 200.0
