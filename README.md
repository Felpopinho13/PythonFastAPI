# API de Pedidos com FastAPI

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Banco%20de%20dados-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

API REST para cadastro e autenticação de usuários e gerenciamento de pedidos e seus itens. O projeto foi construído com FastAPI, usa JWT para autenticação, SQLAlchemy como ORM, SQLite como banco de dados e Alembic para controle de migrações.

## Recursos

- Cadastro de usuários com senha protegida por hash BCrypt.
- Login por JSON ou pelo fluxo OAuth2 Password Bearer.
- Emissão de *access token* JWT e *refresh token*.
- Criação, consulta, cancelamento e finalização de pedidos.
- Inclusão e remoção de itens de um pedido, com cálculo do preço total.
- Listagem de pedidos do usuário autenticado e visão administrativa de todos os pedidos.
- Documentação interativa gerada automaticamente pelo FastAPI.
- Versionamento do esquema do banco com Alembic.

## Tecnologias

- [Python](https://www.python.org/) 3.11+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) e [SQLite](https://www.sqlite.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [python-jose](https://python-jose.readthedocs.io/), [Passlib](https://passlib.readthedocs.io/) e BCrypt

## Pré-requisitos

- Python 3.11 ou superior
- `pip`
- Git (opcional, para clonar o repositório)

## Como executar

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/Felpopinho13/PythonFastAPI.git
cd PythonFastAPI
```

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux, a ativação é:

```bash
source .venv/bin/activate
```

Instale as dependências utilizadas pela aplicação:

```bash
python -m pip install fastapi "uvicorn[standard]" sqlalchemy sqlalchemy-utils alembic python-dotenv "passlib[bcrypt]" "python-jose[cryptography]" python-multipart
```

Crie um arquivo `.env` na raiz do projeto. Use valores próprios; o exemplo abaixo não deve ser usado em produção:

```env
SECRET_KEY=troque-por-uma-chave-longa-e-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=30
```

Para iniciar um banco vazio a partir das migrações, execute:

```bash
alembic upgrade head
```

Por fim, inicie o servidor de desenvolvimento:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

## Documentação interativa

Com a aplicação em execução, acesse:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Na Swagger UI, clique em **Authorize** e informe o token obtido no login. O fluxo OAuth2 utiliza `POST /auth/login-form`; no campo `username`, informe o e-mail do usuário.

## Variáveis de ambiente

| Variável | Descrição | Exemplo |
| --- | --- | --- |
| `SECRET_KEY` | Chave usada para assinar e validar JWTs. | `uma-chave-aleatoria-e-segura` |
| `ALGORITHM` | Algoritmo de assinatura do JWT. | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTE` | Validade, em minutos, do *access token*. | `30` |

## Autenticação

O login retorna dois tokens:

- `access_token`: use no cabeçalho `Authorization: Bearer <token>` para acessar as rotas protegidas.
- `refresh_token`: token emitido com validade de sete dias. Envie-o como Bearer para `GET /auth/refresh` a fim de gerar um novo *access token*.

Todas as rotas sob `/order` exigem autenticação. Algumas operações também verificam se o usuário é administrador ou proprietário do pedido.

## Endpoints

### Autenticação e usuários

| Método | Rota | Autenticação | Descrição |
| --- | --- | --- | --- |
| `GET` | `/auth/` | Não | Verifica a rota de autenticação. |
| `POST` | `/auth/criar_conta` | Não | Cria uma conta de usuário. |
| `POST` | `/auth/login` | Não | Faz login com corpo JSON. |
| `POST` | `/auth/login-form` | Não | Faz login com formulário OAuth2. |
| `GET` | `/auth/refresh` | Bearer | Gera um novo *access token*. |

### Pedidos

| Método | Rota | Regra de acesso | Descrição |
| --- | --- | --- | --- |
| `GET` | `/order/` | Usuário autenticado | Verifica a rota de pedidos. |
| `POST` | `/order/pedido` | Usuário autenticado | Cria um pedido. |
| `GET` | `/order/pedido/{id_pedido}` | Dono ou administrador | Consulta um pedido. |
| `POST` | `/order/pedido/adicionar-item/{id_pedido}` | Dono ou administrador | Adiciona um item ao pedido. |
| `POST` | `/order/pedido/remover-item/{id_item_pedido}` | Dono ou administrador | Remove um item do pedido. |
| `GET` | `/order/listar/pedidos-usuario` | Usuário autenticado | Lista os pedidos do usuário atual. |
| `GET` | `/order/list` | Administrador | Lista todos os pedidos. |
| `POST` | `/orderpedido/cancelar/{id_pedido}` | Dono ou administrador | Cancela um pedido. |
| `POST` | `/orderpedido/finalizar/{id_pedido}` | Dono ou administrador | Finaliza um pedido. |

> **Atenção às duas últimas rotas:** os caminhos acima refletem a implementação atual. Como os decoradores não possuem uma `/` inicial, o prefixo `/order` é concatenado a `pedido`. Para adotar os caminhos convencionais `/order/pedido/cancelar/...` e `/order/pedido/finalizar/...`, é necessário ajustar os decoradores em `order_routes.py`.

## Exemplos de uso

Os exemplos usam PowerShell e consideram a API em execução localmente.

### 1. Criar uma conta

```powershell
$baseUrl = "http://127.0.0.1:8000"

Invoke-RestMethod -Method Post -Uri "$baseUrl/auth/criar_conta" `
  -ContentType "application/json" `
  -Body '{
    "nome": "Maria Silva",
    "email": "maria@example.com",
    "senha": "senha-segura",
    "ativo": true,
    "admin": false
  }'
```

### 2. Fazer login

```powershell
$login = Invoke-RestMethod -Method Post -Uri "$baseUrl/auth/login" `
  -ContentType "application/json" `
  -Body '{
    "email": "maria@example.com",
    "senha": "senha-segura"
  }'

$token = $login.access_token
$headers = @{ Authorization = "Bearer $token" }
```

### 3. Criar um pedido

Informe o ID do usuário que será associado ao pedido:

```powershell
Invoke-RestMethod -Method Post -Uri "$baseUrl/order/pedido" `
  -Headers $headers `
  -ContentType "application/json" `
  -Body '{ "usuario": 1 }'
```

### 4. Adicionar um item

```powershell
Invoke-RestMethod -Method Post -Uri "$baseUrl/order/pedido/adicionar-item/1" `
  -Headers $headers `
  -ContentType "application/json" `
  -Body '{
    "quantidade": 2,
    "sabor": "Calabresa",
    "tamanho": "Grande",
    "preco_unitario": 49.90
  }'
```

### 5. Consultar os próprios pedidos

```powershell
Invoke-RestMethod -Method Get -Uri "$baseUrl/order/listar/pedidos-usuario" -Headers $headers
```

## Estrutura do projeto

```text
.
├── alembic/                         # Ambiente e versões das migrações
│   ├── env.py
│   └── versions/
├── database/
│   └── banco.db                      # Banco SQLite local
├── auth_routes.py                   # Rotas de cadastro, login e renovação de token
├── dependencies.py                  # Sessão do banco e validação de JWT
├── main.py                          # Aplicação FastAPI e configurações principais
├── models.py                        # Modelos SQLAlchemy
├── order_routes.py                  # Rotas de pedidos e itens
├── schemas.py                       # Schemas Pydantic de entrada e resposta
└── alembic.ini                      # Configuração do Alembic
```

## Modelo de dados

```text
Usuario (1) ──── (N) Pedido (1) ──── (N) ItemPedido

Usuario:    id, nome, email, senha, ativo, admin
Pedido:     id, status, usuario, preco
ItemPedido: id, quantidade, sabor, tamanho, preco_unitario, pedido
```

O preço de um pedido é calculado pela soma de `quantidade × preco_unitario` de seus itens. Os status utilizados atualmente são `PENDENTE`, `CANCELADO` e `FINALIZADO`.

## Migrações

O Alembic registra as alterações do esquema em `alembic/versions/`.

```bash
# Aplicar todas as migrações pendentes
alembic upgrade head

# Gerar uma migração após alterar os modelos
alembic revision --autogenerate -m "descricao da alteracao"

# Reverter a última migração
alembic downgrade -1
```

## Segurança

- Nunca publique uma `SECRET_KEY` real. Gere uma chave aleatória longa para cada ambiente.
- O arquivo `.env` não deve ser versionado. Antes de publicar ou compartilhar o repositório, remova-o do controle do Git e inclua `.env` no `.gitignore`.
- Use HTTPS, uma chave forte e uma estratégia de rotação de tokens em ambientes de produção.
- O SQLite é adequado para estudo e desenvolvimento local; para produção, considere um banco gerenciado como PostgreSQL.

## Melhorias futuras

- Criar um `requirements.txt` ou `pyproject.toml` com versões fixadas.
- Adicionar testes automatizados para autenticação, permissões e pedidos.
- Validar que o usuário informado na criação do pedido corresponde ao usuário autenticado.
- Padronizar respostas, códigos de status e mensagens de erro.
- Adicionar paginação à listagem administrativa de pedidos.
- Configurar CORS, logs estruturados e variáveis específicas por ambiente.

## Como contribuir

1. Faça um *fork* do projeto.
2. Crie uma branch: `git checkout -b feat/minha-melhoria`.
3. Implemente a alteração e valide a aplicação localmente.
4. Faça um commit descritivo: `git commit -m "feat: adiciona minha melhoria"`.
5. Envie a branch e abra um Pull Request.

## Autor

Desenvolvido por [Felpopinho13](https://github.com/Felpopinho13).

## Licença

Este repositório ainda não declara uma licença. Caso queira permitir reutilização do código, adicione um arquivo `LICENSE` (por exemplo, MIT).
