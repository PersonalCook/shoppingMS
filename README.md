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
