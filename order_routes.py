from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/order", tags=["order"]) # Cria o roteador para as rotas de pedidos

# Decorator (@): atribui uma função diferente a função que está sendo decorada. 
# Neste caso, a função pedidos() será chamada quando a rota padrão de order for acessada com o método GET.
@order_router.get("/") 
async def pedidos():
    
    # Isto é uma Docstring, que é uma string de documentação para a função.
    """
    Esta é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"message": "Você acessou a rota de pedidos"} # Toda comunicação em APIRest é feita através de JSON

@order_router.post("/pedidos")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session=Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario) # Cria um novo pedido com o id do usuário passado na requisição.
    session.add(novo_pedido) # Adiciona o novo pedido na sessão do banco de dados.
    session.commit() # Salva as alterações no banco de dados.
    return {"Mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"} 