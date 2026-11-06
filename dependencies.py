from fastapi import Depends, HTTPException
from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # O Yield retorna a sessao sem encerrar a função, permitindo que a sessão seja usada em outras partes do código.
    
    # O Finally é executado após o try, mesmo que ocorra um erro no try. Ele garante que a sessão seja fechada após o uso.
    finally:
        session.close() # Fecha a sessão de conexão com o banco de dados após o uso.
        
# Verificar token
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do Token")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido!")
    return usuario
