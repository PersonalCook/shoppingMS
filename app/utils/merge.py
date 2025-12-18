def merge_ingredients(ingredients:list):
    merged = {}
    for item in ingredients:
        key = (item["name"], item["unit"]) 

        if key not in merged:
            merged[key] = 0

        merged[key] += float(item.get("quantity", item.get("amount", 0)))



    result = []

    for (name, unit), quantity in merged.items():
        result.append({
            "name": name,
            "quantity": quantity,
            "unit": unit
        })

    return result
