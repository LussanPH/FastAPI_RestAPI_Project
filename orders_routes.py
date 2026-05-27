from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from dependencies import fetch_session, token_verification
from models import Pedido, Usuario, ItemPedido
from typing import List



orders_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(token_verification)])


@orders_router.get("/")
async def orders():
    """
    Mostra a rota que o usuário se encontra
    """
    return {"mensagem":"Você entrou ná aba de pedidos."}


@orders_router.post("/create_orders")
async def create_order(pedido_schema : PedidoSchema, session : Session = Depends(fetch_session)):
    usuario = session.query(Usuario).filter(Usuario.id == pedido_schema.id_usuario).first()

    if usuario:
        novo_pedido = Pedido(usuario = pedido_schema.id_usuario)
        session.add(novo_pedido)
        session.commit()
        return {"mensagem":f"Pedido criado com sucesso! ID do pedido : {novo_pedido.id}"}
    else:
        raise HTTPException(status_code=400, detail="Usuário não encontrado no banco de dados!")


@orders_router.post("/cancel_orders/{id_pedido}")
async def cancel_order(id_pedido : int, session : Session = Depends(fetch_session), usuario : Usuario = Depends(token_verification)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para cancelar esse pedido.")
    
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem" : f"Pedido {pedido.id} cancelado com sucesso!",
        "pedido" : pedido
    }


@orders_router.get("/list")
async def list_orders(session : Session = Depends(fetch_session), usuario : Usuario = Depends(token_verification)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa operação.")
    
    pedidos = session.query(Pedido).all()

    return {
        "pedidos" : pedidos
    }


@orders_router.post("/add_item/{id_pedido}")
async def add_item(id_pedido : int,    
                    item_pedido_schema : ItemPedidoSchema, 
                    session : Session = Depends(fetch_session), 
                    usuario : Usuario = Depends(token_verification)):
    
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido inexistente.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para adicionar um item a esse pedido.")
    
    item_pedido = ItemPedido(quantidade=item_pedido_schema.quantidade,
                             sabor=item_pedido_schema.sabor,
                             tamanho=item_pedido_schema.tamanho,
                             preco_unitario=item_pedido_schema.preco_unitario,
                             pedido=id_pedido
                             )

    session.add(item_pedido)
    pedido.price_calculator()
    session.commit()

    return {
        "mensagem": "Item craido com sucesso!",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }


@orders_router.post("/remove_item/{id_item_pedido}")
async def add_item(id_item_pedido : int,     
                    session : Session = Depends(fetch_session), 
                    usuario : Usuario = Depends(token_verification)):
    
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item não existente no pedido.")
    
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para adicionar um item a esse pedido.")

    session.delete(item_pedido)
    pedido.price_calculator()
    session.commit()

    return {
        "mensagem": "Item deletado com sucesso!",
        "item_id_removido": item_pedido.id,
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido_atualizado": pedido
    }


@orders_router.post("/finalize_order/{id_pedido}")
async def add_item(id_pedido : int,     
                    session : Session = Depends(fetch_session), 
                    usuario : Usuario = Depends(token_verification)):
    
    pedido = session.query(Pedido).filter(ItemPedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente no banco de dados.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para adicionar um item a esse pedido.")

    pedido.status = "FINALIZADO"
    session.commit()

    return {
        "mensagem": "Pedido finalizado com sucesso!",
        "id_pedido": pedido.id,
        "pedido": pedido
    }


@orders_router.get("/order/{id_pedido}")
async def get_order(id_pedido: int,
                    session : Session = Depends(fetch_session), 
                    usuario : Usuario = Depends(token_verification)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente no banco de dados.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para adicionar um item a esse pedido.")
    
    return{
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }


@orders_router.get("/list/user_orders", response_model=List[ResponsePedidoSchema])
async def list_orders(session : Session = Depends(fetch_session), usuario : Usuario = Depends(token_verification)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).first()

    return pedidos