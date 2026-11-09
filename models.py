from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey # Permite criar o banco de dados
from sqlalchemy.orm import declarative_base, relationship # Permite criar a base do banco de dados
from sqlalchemy_utils.types import ChoiceType # Permite criar campos com textos fixos limitados (como status de pedido)

db = create_engine("sqlite:///database/banco.db") # Cria a conexão com o banco de dados
Base = declarative_base() # Cria a base do banco de dados

# Cria a tabela de USUARIOS no banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)
    
    # O CONSTRUTOR init obriga a passar os parâmetros para criar um novo usuário
    def __init__(self, nome, email, senha, ativo=True, admin=False): 
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
        
# Cria a tabela de PEDIDOS no banco de dados
class Pedido(Base):
    __tablename__ = "pedidos"
    
    # STATUS_PEDIDOS = (
    #     # (CHAVE = Armazenamento no banco, VALOR = Texto que será exibido para o usuário)
    #     ("PENDENTE", "PENDENTE"), 
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # Pendente, Cancelado, Finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id")) # Chave estrangeira para a tabela de usuários
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete") # Efeito cascata, deleta todos os dados relacionados ao item
    # itens =
    
    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status
        
    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        
# Cria a tabela de ITENSPEDIDO no banco de dados
class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id")) # Chave estrangeira para a tabela de pedidos
    
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
        
