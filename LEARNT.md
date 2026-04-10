# Aprendizados do laboratório de Scaling Reads

Este documento resume os principais aprendizados obtidos durante a implementação prática de um laboratório de **scaling reads** com **FastAPI**, **PostgreSQL** e **Redis**.

## Objetivo da atividade

O objetivo principal foi entender, na prática, como funciona uma arquitetura voltada para sistemas com muitas leituras, explorando padrões e componentes comuns em cenários de **scaling reads**.

Além de estudar os conceitos, a atividade também ajudou a consolidar conhecimentos de backend e integração entre aplicação, banco de dados, cache e réplica de leitura.

---

## Principais aprendizados

## 1. Criação de APIs com FastAPI

Durante a atividade, foi possível aprender a construir uma API com **FastAPI** desde o início, entendendo melhor:

- como estruturar uma aplicação simples
- como criar rotas
- como trabalhar com endpoints de CRUD
- como usar `APIRouter`
- como separar melhor responsabilidades entre arquivos da aplicação
- como usar o Swagger automático gerado pelo framework

Também ficou mais claro o papel do **Uvicorn** como servidor ASGI responsável por executar a aplicação FastAPI.

---

## 2. Entendimento maior sobre Pydantic

A atividade também ajudou a entender melhor o uso do **Pydantic** na modelagem de dados da API.

Principais pontos aprendidos:

- definição de schemas de entrada e saída
- validação automática de dados recebidos nas requisições
- diferença entre models de request e models de response
- uso do `model_validate`
- uso de `ConfigDict(from_attributes=True)` para integração com objetos ORM

Esse aprendizado foi importante para perceber que os schemas da API não são necessariamente os mesmos objetos usados na persistência.

---

## 3. Entendimento sobre SQLAlchemy, psycopg e integração com banco de dados

Um dos aprendizados mais importantes foi entender melhor como funciona a integração entre uma aplicação FastAPI e o banco de dados usando **SQLAlchemy** e **psycopg**.

### Sobre o psycopg
Foi entendido que o **psycopg** é o driver responsável por permitir que a aplicação Python se comunique com o PostgreSQL.

### Sobre o SQLAlchemy
Foi possível aprender melhor o papel do **SQLAlchemy**, incluindo:

- criação da engine
- criação da session
- uso do `sessionmaker`
- uso da `Base`
- criação de models ORM
- persistência de dados com `add`, `commit`, `refresh` e `delete`
- consultas ao banco com `select`
- busca por chave primária com `db.get(...)`

### Sobre integração com FastAPI
Também ficou mais claro como integrar o banco com o FastAPI através de:

- dependências com `Depends`
- função `get_db`
- abertura e fechamento de sessão por request

Esse foi um ponto especialmente importante, porque ajudou a entender melhor uma parte que frameworks como Django e Spring Boot normalmente abstraem bastante.

---

## 4. Compreensão mais prática sobre cache, Redis e scaling reads

A atividade permitiu implementar, na prática, um mecanismo de cache usando **Redis**, aplicando o padrão **cache-aside**.

### O que foi aprendido com isso
- como armazenar dados em cache por chave
- como definir uma estratégia simples de TTL
- como consultar o cache antes de acessar o banco
- como popular o cache em caso de miss
- como invalidar o cache após operações de escrita

Esse passo foi importante para entender como reduzir a pressão de leitura sobre o banco principal.

---

## 5. Compreensão sobre primary, replica e read/write split

Outro aprendizado central foi entender melhor o uso de:

- **primary database** para escritas
- **replica database** para leituras

Mesmo com uma réplica fake/local para fins de laboratório, foi possível visualizar bem o conceito de **read/write split**, separando:

- `POST`, `PUT`, `DELETE` -> primary
- `GET` -> cache / replica

Isso ajudou a consolidar o entendimento de que scaling reads não depende apenas de cache, mas também pode envolver bancos separados para leitura e escrita.

---

## 6. Entendimento sobre consistência eventual e dados defasados

Ao implementar o fluxo com primary e replica, ficou mais claro um dos principais trade-offs dessa arquitetura:

- a réplica pode não refletir imediatamente o estado mais recente do primary
- leituras podem retornar dados desatualizados
- isso é um exemplo de **consistência eventual**

Esse aprendizado foi importante porque mostra que escalar leitura normalmente traz ganhos de desempenho e capacidade, mas também aumenta a complexidade e exige decisões sobre consistência.

---

## 7. Evolução da visão de arquitetura

Além da implementação técnica, a atividade ajudou a entender melhor como pensar uma arquitetura de scaling reads em camadas.

Foi possível visualizar de forma mais concreta:

- o caminho de escrita
- o caminho de leitura
- a função do cache
- a função da réplica
- o papel da invalidação de cache
- os trade-offs envolvidos

Também ajudou a entender melhor como desenhar e explicar esse tipo de arquitetura em entrevistas ou discussões de system design.

---

## Resumo final

De forma geral, esta atividade ajudou a consolidar conhecimentos importantes de backend e arquitetura, principalmente em torno de sistemas orientados a leitura.

### Principais tópicos aprendidos
- criação de APIs com FastAPI
- uso de Pydantic para validação e schemas
- integração com PostgreSQL usando SQLAlchemy e psycopg
- uso de Redis como camada de cache
- implementação de cache-aside
- separação entre read path e write path
- uso de primary e replica
- entendimento de consistência eventual e replica lag
- visão mais concreta sobre soluções de scaling reads

---

## Próximos passos possíveis

Como continuação desse aprendizado, alguns próximos passos interessantes seriam:

- implementar fallback de leitura da replica para o primary
- adicionar métricas de cache hit e cache miss
- criar um read model otimizado para listagens
- simular carga para comparar cenários com e sem cache
- testar replicação real em vez de réplica fake