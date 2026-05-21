from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    Mostra a rota que o usuário se encontra.
    """
    return {"mensagem":"Você entrou na aba de autorização. Somente pessoas autorizadas acessam aqui.", "autorizado": False}