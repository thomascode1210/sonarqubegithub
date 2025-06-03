from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import init_db 
from app.api.router import api_router
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield  

app = FastAPI(docs_url="/docs", lifespan=lifespan)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins_list = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

if not allowed_origins_list:
    allowed_origins_list = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins_list,
    allow_credentials=True,
    # allow_origins=[], 
    # allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "POSX API ready!"}