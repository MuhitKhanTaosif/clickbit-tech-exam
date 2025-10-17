from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session
from db import create_db_and_tables


import localAuth
import userRoutes



app = FastAPI()
# app.mount("/resource", StaticFiles(directory="resource"), name="resource")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "0.0.0.0"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(localAuth.router)
app.include_router(userRoutes.router)

@app.get("/")
async def root():
    return {"message": "FastAPI application running"}

