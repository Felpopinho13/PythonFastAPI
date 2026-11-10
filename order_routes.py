from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)]) 
# Cria o roteador para as rotas de pedidos e quando a dependencia passa no router, todas as funções recebem ela.

# Decorator (@): atribui uma função diferente a função que está sendo decorada. 
# Neste caso, a função pedidos() será chamada quando a rota padrão de order for acessada com o método GET.
@order_router.get("/") 
async def pedidos():
    
    # Isto é uma Docstring, que é uma string de documentação para a função.
    """
    Esta é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"message": "Você acessou a rota de pedidos"} # Toda comunicação em APIRest é feita através de JSON

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session=Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario) # Cria um novo pedido com o id do usuário passado na requisição.
    session.add(novo_pedido) # Adiciona o novo pedido na sessão do banco de dados.
    session.commit() # Salva as alterações no banco de dados.
    return {"Mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"} 

@order_router.post("pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session : Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    # Procedimento para apenas usuário admin fazer a ação
    if not usuario.admin and usuario.id != pedido.usuario: 
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "Mensagem": f"Pedido número {pedido.id} cancelado com sucesso",
        "Pedido": pedido
    }
    
@order_router.get("/list")
async def listar_pedidos(session : Session = Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all() # Verificar a integridade do sistema caso for muito grande
        return {
            "Pedidos" : pedidos 
        }
        
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido : int,
                                item_pedido_schema: ItemPedidoSchema, 
                                session : Session = Depends(pegar_sessao),
                                usuario : Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existe")
    if not usuario.admin and usuario.id != pedido.usuario: 
        raise HTTPException(status_code=401, detail="Voce não tem autorização pra fazer essa operação")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "Mensagem" : "Item criado com sucesso",
        "item_id" : item_pedido.id,
        "preço do pedido" : pedido.preco
        }
    
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido : int,
                                session : Session = Depends(pegar_sessao),
                                usuario : Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existe")
    if not usuario.admin and usuario.id != pedido.usuario: 
        raise HTTPException(status_code=401, detail="Voce não tem autorização pra fazer essa operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "Mensagem" : "Item removido com sucesso",
        "quantidade_itens_pedido" : len(pedido.itens),
        "pedido" : pedido
        }
    
    
@order_router.post("pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session : Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario: 
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "Mensagem": f"Pedido número {pedido.id} finalizado com sucesso",
        "Pedido": pedido
    }
    
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session : Session = Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    return{
        "Quantidade de itens do pedido": len(pedido.itens),
        "pedido" : pedido
    }