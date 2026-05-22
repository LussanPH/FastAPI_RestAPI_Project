from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from models import db, Usuario

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    Mostra a rota que o usuário se encontra.
    """
    return {"mensagem":"Você entrou na aba de autorização. Somente pessoas autorizadas acessam aqui.", "autorizado": False}

@auth_router.post("/create_user")
async def create_user(email:str, senha:str, nome:str):
    Session = sessionmaker(bind=db)
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if usuario:
        return {"mensagem":"Já existe um usuário com esse email"}
    else:
        usuario_novo = Usuario(nome, email, senha)
        session.add(usuario_novo)
        session.commit()
        return {"mensagem":"Usuário criado com sucesso!"}