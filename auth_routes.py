from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import fetch_session
from password_crypto import get_hashed_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    Mostra a rota que o usuário se encontra.
    """
    return {"mensagem":"Você entrou na aba de autorização. Somente pessoas autorizadas acessam aqui.", "autorizado": False}

@auth_router.post("/create_user")
async def create_user(email:str, senha:str, nome:str, session = Depends(fetch_session)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado!")
    else:
        senha_criptograda = get_hashed_password(senha)
        usuario_novo = Usuario(nome, email, senha_criptograda)
        session.add(usuario_novo)
        session.commit()
        return {"mensagem":"Usuário criado com sucesso!"}