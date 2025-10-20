from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from motor import motor_asyncio
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from collections import defaultdict
from starlette.staticfiles import StaticFiles
from .config import BaseConfig
from ..routers.cars import router as cars_router
# from routers.users import router as users_router
from pathlib import Path
import os

settings = BaseConfig()

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"
(STATIC_DIR / "uploads").mkdir(parents=True, exist_ok=True)

async def lifespan(app: FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]
    try:
        await app.client.admin.command("ping")
        print("Pinged your deployment. You have successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    yield
    app.client.close()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(cars_router, prefix="/cars", tags=["cars"])

@app.get("/")
async def get_root():
    return {"Message": "Root working!"}