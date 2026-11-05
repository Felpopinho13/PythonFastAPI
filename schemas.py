from pydantic import BaseModel # Pydantic é uma biblioteca de validação de dados que permite criar modelos de dados com validação automática.
from typing import Optional # Importa o tipo Optional do módulo typing, que permite definir campos opcionais em modelos de dados.

# Define o schema de usuário para validação dos dados recebidos na requisição.
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    
    # Define a configuração do schema para permitir a criação de instâncias a partir de objetos ORM (Object-Relational Mapping).
    class Config:
        from_attributes = True
        
class PedidoSchema(BaseModel):
    usuario: int
    
    class Config:
        from_attributes = True