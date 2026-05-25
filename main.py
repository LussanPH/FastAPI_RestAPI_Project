from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")

from orders_routes import orders_router
from auth_routes import auth_router

app.include_router(orders_router)
app.include_router(auth_router)