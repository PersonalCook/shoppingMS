from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import shopping
from . import models
from .database import engine

app = FastAPI(title="Shopping Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(shopping.router)


@app.get("/")
def root():
    return {"msg": "Shopping Service running in Docker!"}