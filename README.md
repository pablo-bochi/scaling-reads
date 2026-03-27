# Scaling Reads Lab

Projeto simples para estudar, na prática, padrões de **scaling reads** em uma API de produtos usando **FastAPI**, **PostgreSQL** e **Redis**.

## Objetivo

Explorar de forma hands on alguns conceitos importantes de system design voltados para sistemas com muitas leituras, como:

- cache-aside com Redis
- separação entre read path e write path
- uso de primary e replica
- consistência eventual
- invalidação de cache

## Arquitetura

Atualmente o projeto segue esta ideia:

- **POST / PUT / DELETE** escrevem no **Postgres Primary**
- **GET** lêem do **Redis** primeiro
- em caso de cache miss, a leitura vai para o **Postgres Replica**
- a replica é sincronizada manualmente para fins de laboratório

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Docker Compose

## Estrutura do projeto

```text
app/
├── main.py
├── db.py
├── cache.py
├── models.py
├── schemas.py
└── routes/
    ├── health.py
    ├── products.py
    └── admin.py
