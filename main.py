from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

from orders_routes import orders_router
from auth_routes import auth_router

app.include_router(orders_router)
app.include_router(auth_router)