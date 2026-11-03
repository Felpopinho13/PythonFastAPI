from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"]) #Cria o roteador para as rotas de autenticação

# Decorator (@): atribui uma função diferente a função que está sendo decorada. 
# Neste caso, a função autenticar() será chamada quando a rota padrão de auth for acessada com o método GET.
@auth_router.get("/")
async def autenticar():
    
    # Isto é uma Docstring, que é uma string de documentação para a função.
    """
    Esta é a rota padrão de autenticação do nosso sistema.
    """
    # Toda comunicação em APIRest é feita através de JSON
    return {"Message": "Você acessou a rota padrão de autenticação", "Autenticado": False}