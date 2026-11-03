from fastapi import APIRouter

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
