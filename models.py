import enum
from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite///banco.db", echo=True)

Base = declarative_base()

class Status_pedido(enum.Enum):
    PENDENTE: "PENDENTE"
    CANCELADO: "CANCELADO"
    FINALIZADO: "FINALIZADO"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, senha, ativo=True, admin=False):
        self.name = name
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", Enum(Status_pedido), default=Status_pedido.PENDENTE)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    #itens = 

    def __init__(self, status=Status_pedido.PENDENTE, usuario, preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco