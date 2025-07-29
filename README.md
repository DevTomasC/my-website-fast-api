# 🍽️ My Website - FastAPI

Esse projeto é um **exemplo lúdico de compreensão e estudo do Framework FastAPI**, e também pode ser usado como template para novos projetos.  
Desenvolvido por: [DevTomasC](https://github.com/DevTomasC)

---

## 👋 Wellcome! :D

---

## ⚙️ Funcionamento geral — Modelo de aplicação: *Cardápio Digital*

### 🔁 Fluxo de um pedido (com explicação técnica e arquitetural)

#### 🧑‍💻 1. **Client (Frontend ou App móvel)**

> Envia requisição HTTP POST para o endpoint `/pedido` com:
- Payload JSON com dados do pedido (itens, quantidade, observações).
- Header `Authorization: Bearer <token>` contendo o JWT.

#### 🌀 2. **Uvicorn (ASGI Server)**

> Recebe requisição assíncrona, faz parsing e roteia para a aplicação FastAPI.

#### ⚡ 3. **FastAPI (Framework Web)**

> - Recebe JSON e JWT do header.
- Utiliza Pydantic para validação automática dos dados.
- Garante que os dados recebidos sejam coerentes (ex: quantidade > 0).

#### 🧱 4. **Pydantic (Validação de dados)**

> - Converte JSON para objetos Python fortemente tipados.
- Rejeita requisições inválidas (erro HTTP 422).

#### 🔐 5. **PyJWT (Autenticação)**

> - Decodifica e valida o token JWT (assinatura, expiração, claims).
- Confirma que o usuário está autenticado e autorizado.

#### 🧠 6. **Business Logic (Camada de serviço)**

> - Valida o estoque via SQLAlchemy.
- Calcula valor total.
- Aplica regras (ex: estoque insuficiente retorna HTTP 400 ou 409).
- Prepara instâncias ORM para inserir no banco.

#### 🛢️ 7. **SQLAlchemy (ORM)**

> - Executa INSERT do pedido.
- Atualiza estoque.
- Usa transações (rollback em caso de erro).

#### 📐 8. **Alembic (Migrações)**

> - Garante estrutura de banco sincronizada com o código.
- Aplica migrações automaticamente.

#### 🔒 9. **Passlib**

> Usado apenas para hashing e verificação de senhas na autenticação (login/registro).

#### 🧪 10. **pytest (Testes)**

> Testa:
- Validação Pydantic
- Token JWT
- Regras de negócio (estoque, pedidos)
- Endpoints (via `TestClient`)
- Rollback e transações

---

## 🧱 Arquitetura técnica (MVC simplificado)

- **Model**: Pydantic + SQLAlchemy  
- **View**: JSON API via FastAPI  
- **Controller**: routers + business logic

---

## 🔁 Resumo técnico dos componentes

| Componente     | Função principal                                   |
|----------------|----------------------------------------------------|
| **Uvicorn**    | Servidor ASGI que roda o app FastAPI               |
| **FastAPI**    | Framework principal (validação, rotas, responses)  |
| **Pydantic**   | Tipagem e validação automática                     |
| **JWT (PyJWT)**| Autenticação stateless via token                   |
| **SQLAlchemy** | ORM e transações com banco                         |
| **Alembic**    | Migrações automáticas do banco                     |
| **Passlib**    | Segurança das senhas (hash)                        |
| **pytest**     | Testes unitários e de integração                   |

---

## 📈 Diagrama UML ASCII (resumo da comunicação dos componentes)

```text
+-------------------+
|    Client         |
| (Browser, App)    |
+---------+---------+
          |
          | HTTP Request (JSON, JWT, etc)
          v
+---------+---------+             +-----------------+
|     Uvicorn       | <---------> |  Database       |
| (ASGI Server)     |             | (PostgreSQL etc)|
+---------+---------+             +-----------------+
          |
          | Passa requisição
          v
+-------------------+
|     FastAPI       |  <-------------------------------------------+
|  (Framework)      |                                            |
+---------+---------+                                            |
          |                                                      |
          | Recebe dados JSON                                    |
          v                                                      |
+-------------------+          +----------------+                |
|   Pydantic        |          | SQLAlchemy ORM |                |
| (Validação &      |          | (Query Builder)|                |
|  Parsing)         |          +--------+-------+                |
+---------+---------+                   |                        |
          |                           | Executa comandos SQL     |
          | Dados validados           |                          |
          v                           v                          |
+-------------------+        +-------------------+               |
| Business Logic /  |        | Alembic           |               |
| Controllers       |        | (Migrações do DB) |               |
+---------+---------+        +-------------------+               |
          |                                                      |
          v                                                      |
+-------------------+                                            |
| Passlib           | (Hash senhas e valida senhas)              |
+-------------------+                                            |
          |                                                      |
          v                                                      |
+-------------------+                                            |
| PyJWT             | (Cria / valida tokens JWT)                 |
+-------------------+                                            |
          |                                                      |
          v                                                      |
+-------------------+                                            |
| pytest            | (Testa todas as partes acima)              |
+-------------------+                                            |
                                                                 |
                                                                 |
   <-----------------------------------------------------------+
