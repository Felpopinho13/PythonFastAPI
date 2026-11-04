from fastapi import APIRouter, Depends
from models import Usuario # Importa o modelo de usuário do arquivo models.py
from dependencies import pegar_sessao # Importa a função pegar_sessao() do arquivo dependencies.py
from main import bcrypt_context # Importa o contexto de criptografia de senhas do arquivo main.py

auth_router = APIRouter(prefix="/auth", tags=["auth"]) #Cria o roteador para as rotas de autenticação

# Decorator (@): atribui uma função diferente a função que está sendo decorada. 
# Neste caso, a função autenticar() será chamada quando a rota padrão de auth for acessada com o método GET.
@auth_router.get("/")
async def home():
    
    # Isto é uma Docstring, que é uma string de documentação para a função.
    """
    Esta é a rota padrão de autenticação do nosso sistema.
    """
    # Toda comunicação em APIRest é feita através de JSON
    return {"Message": "Você acessou a rota padrão de autenticação", "Autenticado": False}

@auth_router.post("/criar_conta")
# Para criar uma conta, é obrigatório passar o email e a senha do usuário.
# A partir de agora, a sessao vem de fora e nao é passada como função e sim como parametro da função, com o uso do Depends.
async def criar_conta(email: str, senha: str, nome: str, session=Depends(pegar_sessao)): 
    usuario = session.query(Usuario).filter(Usuario.email == email).first() # Verifica se o email já está cadastrado no banco de dados.
    if usuario: 
        # Caso em que já existe um usuário com o email informado
        return{"Mensagem": "Já existe um usuário com esse email"}
    else: 
        senha_criptografada = bcrypt_context.hash(senha) # Criptografa a senha do usuário
        novo_usuario = Usuario(nome, email, senha_criptografada) # Cria um novo usuário com os dados passados na requisição.
        session.add(novo_usuario) # Adiciona o novo usuário na sessão do banco de dados.
        session.commit() # Salva as alterações no banco de dados.
        return {"Mensagem": "Usuário cadastrado com sucesso"}
    
    