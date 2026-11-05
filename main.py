from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

SECRET_KEY = os.getenv("SECRET_KEY") # Obtém a chave secreta do arquivo .env
# A chave secreta é utilizada para criptografar e descriptografar dados sensíveis, misturando a chave com os dados para gerar um hash único.

ALGORITHM = os.getenv("ALGORITHM") # Algoritmo de criptografia 
ACCESS_TOKEN_EXPIRE_MINUTE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE")) # Tempo de sessão de usuário

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Cria um contexto de criptografia para senhas

from auth_routes import auth_router # Importa o arquivo auth_routes.py
from order_routes import order_router # Importa o arquivo order_routes.py

app.include_router(auth_router) # Inclui as rotas de autenticação
app.include_router(order_router) # Inclui as rotas de pedidos

# Utilizado para rodar a aplicação
# uvicorn main:app --reload 