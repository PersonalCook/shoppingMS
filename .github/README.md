CI overview

This repo runs two GitHub Actions jobs:
- test: installs requirements and runs `pytest`
- container: builds the Docker image, starts Postgres, runs the container, and hits `/` for a smoke test

Tests (files and intent):
- `tests/test_crud.py`: database CRUD helpers for shopping carts.
- `tests/test_router_cart.py`: cart API endpoints, auth handling, and recipe lookup flows.
- `tests/test_utils_auth.py`: JWT decode helpers and error cases.
- `tests/test_utils_merge.py`: ingredient merge logic for recipe lists.
