from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router # Importa o arquivo auth_routes.py
from order_routes import order_router # Importa o arquivo order_routes.py

app.include_router(auth_router) # Inclui as rotas de autenticação
app.include_router(order_router) # Inclui as rotas de pedidos

# Utilizado para rodar a aplicação
# uvicorn main:app --reload 