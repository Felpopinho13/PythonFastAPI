from fastapi import APIRouter, Depends, HTTPException
from models import Usuario # Importa o modelo de usuário do arquivo models.py
from dependencies import pegar_sessao # Importa a função pegar_sessao() do arquivo dependencies.py
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTE, SECRET_KEY # Importa o contexto de criptografia de senhas do arquivo main.py
from schemas import UsuarioSchema, LoginSchema # Importa o schema de usuário do arquivo Schemas.py
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"]) #Cria o roteador para as rotas de autenticação

# Criação de token de login
def criar_token(id_usuario):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE) 
    dic_info = {"user_id": id_usuario, "exp": data_expiracao} # Dicionario de sessão
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

# Criação de autenticação de Usuário
def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    
    return usuario


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
async def criar_conta(usuario_schema: UsuarioSchema, session: Session=Depends(pegar_sessao)): 
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first() # Verifica se o email já está cadastrado no banco de dados.
    if usuario: 
        # Caso em que já existe um usuário com o email informado
        raise HTTPException(status_code=400, detail="Email do usuário já foi cadastrado") # Raise: Lança uma exceção HTTP com o status code 400 e a mensagem de erro informando que o email já foi cadastrado.
    else: 
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) # Criptografa a senha do usuário
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin) # Cria um novo usuário com os dados passados na requisição.
        session.add(novo_usuario) # Adiciona o novo usuário na sessão do banco de dados.
        session.commit() # Salva as alterações no banco de dados.
        return {"Mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}
    
# Login de usuário
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session=Depends(pegar_sessao)): 
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code= 400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token,
                "token_type": "Bearer"
                }
    