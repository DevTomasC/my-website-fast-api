# my-website-fast-api
Esse Website é um exemplo lúdico de compreensão e estudo do Framework FastAPI!
     Também serve pra template 
    por: DevTomasC 

# Wellcome!  :D

# Funcionamento do Web em uma aplicação modelo cardápio digital
Fluxo Lúdico com modelo "fazer pedido" explicado com foco técnico e arquitetural:

   # Client (frontend ou app móvel)

        Gera requisição HTTP POST para endpoint /pedido contendo um payload JSON com os dados do pedido (ex: itens, quantidade, observações) e o token JWT no header Authorization: Bearer <token>.

   # Uvicorn (ASGI server)

        Recebe a requisição HTTP assíncrona, faz o parsing do cabeçalho e corpo, encaminha para o FastAPI app conforme roteamento.

   # FastAPI (framework web)

        Pega a requisição e extrai o JSON body e o token JWT.

        Define tipagens (models) Pydantic para validação e parsing automático dos dados recebidos.

        Recebe o objeto Pydantic validado, já garantido que os dados estão coerentes (ex: quantidade é int > 0, itens existem no cardápio).

   # Pydantic

        Valida e converte o JSON para objetos Python fortemente tipados.

        Rejeita requisições malformadas ou com campos inválidos, retornando erro HTTP 422.

   # PyJWT

        Decodifica o token JWT usando a chave secreta do backend.

        Verifica assinatura, expiração, permissões (claims).

        Confirma que o usuário está autenticado e autorizado a fazer pedidos.

   # Business Logic (controller/service layer)

        Recebe o objeto do pedido validado e o usuário autenticado.

        Consulta estoque atual via SQLAlchemy para cada item do pedido.

        Calcula valor total com base nos preços atuais (banco ou cache).

        Verifica se estoque é suficiente; caso contrário, retorna erro HTTP 400 ou 409.

        Cria instâncias ORM para o pedido e seus itens, preparando para inserir no banco.

   # SQLAlchemy (ORM)

        Executa comandos SQL para inserir o pedido na tabela pedidos.

        Atualiza o estoque dos itens na tabela produtos decrementando as quantidades.

        Usa transação para garantir atomicidade: se alguma operação falha, rollback.

   # Alembic (migrações)

        Garante que a estrutura do banco (tabelas, colunas) está atualizada para suportar o esquema do pedido.

        Executa migrações automáticas antes da aplicação iniciar, para evitar inconsistências.

   # Passlib

        Não entra no fluxo do pedido, só usado em login para comparar hash de senha.

   # pytest (testes automatizados)

        Roda testes unitários e de integração:

            Validação Pydantic.

            Decodificação de token JWT.

            Regras da business logic (ex: falha estoque insuficiente).

            Testa endpoints FastAPI simulando requisições.

            Testa rollback do banco em caso de falhas.

   # Resumo técnico da arquitetura [MVC]:

    Uvicorn atua como ASGI server que suporta async nativamente, alta performance.

    FastAPI usa tipagem estática via Pydantic para validar e converter entrada.

    JWT token é verificado para autenticação stateless, não mantém sessão.

    SQLAlchemy gerencia ORM e abstrai SQL, facilitando transações e consultas.

    Alembic mantém versão do banco sincronizada com código.

    Testes garantem confiabilidade e qualidade antes de deploy.

    Passlib só na camada de autenticação para segurança das senhas.



# Ascii UML
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
          |                                                      |
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

