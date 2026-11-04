from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # O Yield retorna a sessao sem encerrar a função, permitindo que a sessão seja usada em outras partes do código.
    
    # O Finally é executado após o try, mesmo que ocorra um erro no try. Ele garante que a sessão seja fechada após o uso.
    finally:
        session.close() # Fecha a sessão de conexão com o banco de dados após o uso.