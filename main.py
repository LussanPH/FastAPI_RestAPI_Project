from fastapi import FastAPI
from orders_routes import orders_router
from auth_routes import auth_router

app = FastAPI()

app.include_router(orders_router)
app.include_router(auth_router)