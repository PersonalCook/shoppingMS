import os
import httpx

RECIPE_SERVICE_URL = os.getenv("RECIPE_SERVICE_URL")

if not RECIPE_SERVICE_URL:
    raise RuntimeError("RECIPE_SERVICE_URL must be set in the environment")

async def get_recipe(recipe_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RECIPE_SERVICE_URL}/{recipe_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


