# shoppingMS

Shopping service for PersonalCook.

---

## Overview
ShoppingMS generates and stores shopping carts based on selected recipes. It aggregates ingredients from the recipe service and merges them into a single list.

---

## Architecture

- **FastAPI** application
- **PostgreSQL** for persistence
- **JWT authentication** for user-scoped carts
- **Recipe service integration** for ingredient retrieval and recipe metadata
- **Social service integration** 
- **Prometheus / Grafana** for metrics and monitoring
- **EFK stack (Fluent Bit, Elasticsearch, Kibana)** for centralized logging

---

## Configuration

The application configuration is fully separated from the implementation and is provided via multiple sources:

### Configuration sources

1. **Kubernetes ConfigMap**
   - Non-sensitive configuration injected as environment variables.
2. **Kubernetes Secrets**
   - Sensitive values such as database credentials and JWT secret.

All configuration values are parametrized via Helm `values.yaml` files.

---

## Environment Variables

| Variable            | Description                                    |
| ------------------- | ---------------------------------------------- |
| DATABASE_URL        | PostgreSQL connection string                   |
| JWT_SECRET          | JWT signing secret                             |
| JWT_ALGORITHM       | JWT algorithm (default: HS256)                 |
| RECIPE_SERVICE_URL  | Recipe service base URL                        |
| SOCIAL_SERVICE_URL  | Social service base URL                        |
| CORS_ORIGINS        | Allowed CORS origins          |

---

## Local development

- Configuration via `.env` file (see `.env.example`)  
- API available at `http://localhost:8004`  
- PostgreSQL available on `localhost:5435`

Steps:
1. Create a Docker network for PersonalCook.
2. Copy `.env.example` to `.env`.
3. Start services using Docker Compose.

---


## Kubernetes

- Configuration via Helm values, ConfigMaps, and Secrets
- API exposed through reverse proxy: http://134.112.128.83/api/shopping/

Separate Helm values files are used:
- `values-dev.yaml`
- `values-prod.yaml`

Example deployments:
helm upgrade --install shopping-service . -n personalcook -f values-prod.yaml

---

## Observability & Logging

ShoppingMS integrates with centralized logging and monitoring.

### Logging

Application logs are written to stdout and collected at the Kubernetes level using:

- **Fluent Bit** – log collection and forwarding
- **Elasticsearch** – centralized log storage and indexing
- **Kibana** – log visualization and analysis

### Metrics & Monitoring

The service exposes Prometheus-compatible metrics at `/metrics`.

Metrics are scraped using:

- **Prometheus Operator** via a `ServiceMonitor`
- Visualized in **Grafana**

#### Exposed metrics

- **`http_requests_total`** _(Counter)_  
  Total number of HTTP requests.  
  **Labels:** `method`, `endpoint`, `status_code`

- **`http_request_errors_total`** _(Counter)_  
  Total number of failed HTTP requests (error responses).  
  **Labels:** `method`, `endpoint`, `status_code`

- **`http_request_latency_seconds`** _(Histogram)_  
  HTTP request latency distribution (seconds).  
  **Labels:** `method`, `endpoint`

- **`http_requests_in_progress`** _(Gauge)_  
  Number of HTTP requests currently being processed.

- **`shopping_carts_created_total`** *(Counter)*  
  Total number of shopping carts created.  
  Labels: `source`, `status`

---

## Dependencies
- recipe service at RECIPE_SERVICE_URL (default http://recipe_service:8000/recipes)
- social service at SOCIAL_SERVICE_URL (default http://social_service:8000)

---

## API Docs
- Swagger UI: http://134.112.128.83/api/shopping/docs
- ReDoc: http://134.112.128.83/api/shopping/redoc
- OpenAPI JSON: http://134.112.128.83/api/shopping/openapi.json

---

## Testing
Run tests locally:
```
pytest
```
---

## CI
This repo runs two GitHub Actions jobs:
- `test`: installs requirements and runs `pytest`
- `container`: builds the Docker image, starts Postgres, runs the container, and hits `/` for a smoke test

Tests (files and intent):
- `tests/test_crud.py`: database CRUD helpers for shopping carts.
- `tests/test_router_cart.py`: cart API endpoints, auth handling, and recipe lookup flows.
- `tests/test_utils_auth.py`: JWT decode helpers and error cases.
- `tests/test_utils_merge.py`: ingredient merge logic for recipe lists.

---

## Troubleshooting
- Recipe service unreachable: verify `RECIPE_SERVICE_URL`.
- JWT errors: verify `JWT_SECRET` and `JWT_ALGORITHM`.
- Database connection errors: verify `DATABASE_URL` and Postgres container status.
