from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependencies import fetch_session, token_verification
from config import ACCESS_TOKEN_EXPIRATE_MINUTES, SECRET_KEY, ALGORITHM
from password_crypto import get_hashed_password, verify_password
from schemas import UsuariosSchema, LoginSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


def create_token(id_usuario, duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRATE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dicionario_informacoes = {"sub" : str(id_usuario), "exp" : data_expiracao}
    if SECRET_KEY and ALGORITHM:
        jwt_codificado = jwt.encode(dicionario_informacoes, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def login_authentication(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not verify_password(senha, usuario.senha):
        return False
    return usuario


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    """
    Mostra a rota que o usuário se encontra.
    """
    return {"mensagem":"Você entrou na aba de autorização. Somente pessoas autorizadas acessam aqui.", "autorizado": False}


@auth_router.post("/create_user")
async def create_user(usuario_schema : UsuariosSchema, session : Session = Depends(fetch_session)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado!")
    else:
        senha_criptograda = get_hashed_password(usuario_schema.senha)
        usuario_novo = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptograda, usuario_schema.ativo, usuario_schema.admin)
        session.add(usuario_novo)
        session.commit()
        return {"mensagem":"Usuário criado com sucesso!"}
    

@auth_router.post("/login")
async def login(login_schema : LoginSchema, session : Session = Depends(fetch_session)):
    usuario = login_authentication(login_schema.email, login_schema.senha, session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha inválida.")
    else:
        access_token = create_token(usuario.id)
        refresh_token = create_token(usuario.id, timedelta(days=7))

        return {"access_token" : access_token, 
                "refresh_token" : refresh_token,
                "type_token" : "Bearer"}


@auth_router.post("/login_form")
async def login_form(dados_formulario : OAuth2PasswordRequestForm = Depends(), session : Session = Depends(fetch_session)):
    usuario = login_authentication(dados_formulario.username, dados_formulario.password, session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha inválida.")
    else:
        access_token = create_token(usuario.id)

        return {"access_token" : access_token,
                "type_token" : "Bearer"}


@auth_router.get("/refresh")
async def create_access_token(usuario:Usuario = Depends(token_verification)):
    access_token = create_token(usuario.id)

    return {"access_token" : access_token, 
            "type_token" : "Bearer"}