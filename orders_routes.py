from fastapi import APIRouter

orders_router = APIRouter(prefix="/orders", tags=["orders"])

@orders_router.get("/")
async def orders():
    """
    Mostra a rota que o usuário se encontra
    """
    return {"mensagem":"Você entrou ná aba de pedidos."}