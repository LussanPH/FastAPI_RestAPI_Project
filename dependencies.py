from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from main import oauth2_schema
from config import SECRET_KEY, ALGORITHM
from models import db
from jose import jwt, JWTError

def fetch_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def token_verification(token:str = Depends(oauth2_schema), session:Session = Depends(fetch_session)):
    if SECRET_KEY and ALGORITHM:
        try:
            dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
            usuario_id = int(dic_info.get("sub"))
        except JWTError:
            raise HTTPException(status_code=401, detail="Acesso Negado")
        
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")

    return usuario

