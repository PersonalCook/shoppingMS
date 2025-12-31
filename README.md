# shoppingMS

Shopping service for PersonalCook.

## Local dev
1. docker network create personalcook-net
2. copy .env.example .env
3. docker compose up --build

## Dependencies
- recipe service at RECIPE_SERVICE_URL (default http://recipe_service:8000/recipes)
- social service at SOCIAL_SERVICE_URL (default http://social_service:8000)

## Ports
- API: 8004
- Postgres: 5435

## API Docs
- Swagger UI: http://localhost:8004/docs
- ReDoc: http://localhost:8004/redoc
- OpenAPI JSON: http://localhost:8004/openapi.json

## CI
This repo runs two GitHub Actions jobs:
- test: installs requirements and runs `pytest`
- container: builds the Docker image, starts Postgres, runs the container, and hits `/` for a smoke test

Tests (files and intent):
- `tests/test_crud.py`: database CRUD helpers for shopping carts.
- `tests/test_router_cart.py`: cart API endpoints, auth handling, and recipe lookup flows.
- `tests/test_utils_auth.py`: JWT decode helpers and error cases.
- `tests/test_utils_merge.py`: ingredient merge logic for recipe lists.
