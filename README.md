# pokeDiary

API desenvolvida com **FastAPI** para criação de um diário de Pokémons, consumindo dados da [PokéAPI](https://pokeapi.co) e permitindo que usuários registrem, organizem e gerenciem suas experiências com diferentes Pokémons.

---

## Sobre o Projeto

O **pokeDiary** é um projeto backend estruturado com foco em **boas práticas de engenharia de software**, arquitetura escalável e integração entre múltiplos serviços.

Mais do que um projeto funcional, ele foi desenvolvido como uma **base sólida para demonstrar domínio técnico** em:

- Desenvolvimento de APIs modernas  
- Arquitetura em camadas (Clean Architecture)  
- Integração com mensageria  
- Containerização e orquestração  
- Pipeline de CI/CD  

A aplicação permite que usuários:

- Criem e gerenciem suas contas  
- Registrem Pokémons em um diário personalizado  
- Consultem informações detalhadas consumidas da PokéAPI  
- Atualizem e removam registros do diário   

---

## Tecnologias Utilizadas

- Python  
- FastAPI  
- PostgreSQL  
- Prisma ORM  
- RabbitMQ (processamento assíncrono)  
- Docker e Docker Compose
- Jenkins (CI/CD) 

---

## Arquitetura do Projeto

O projeto segue uma arquitetura baseada em **Clean Architecture**, promovendo:

- Separação de responsabilidades  
- Baixo acoplamento  
- Alta coesão  
- Facilidade de manutenção e evolução

```bash
pokeDiary/
│
├── controller/     # Rotas da API (camada de entrada)
├── core/            # Definições centrais (ex: roles de usuário)
├── dependencies/    # Injeções de dependência (auth, etc)
│
├── config/          # Configurações da aplicação
│   ├── connection_db.py  # Conexão com banco de dados
│   └── security.py       # Configuração de autenticação e segurança
│
├── messaging/       # Integração com RabbitMQ (producers/consumers)
│
├── model/          # Modelos de domínio (User, Diary)
├── Prisma/          # Schema e client Prisma
├── repository/    # Acesso aos dados (camada de persistência)
├── services/        # Regras de negócio
├── schemas/         # Schemas (validação e resposta)
│
├── main.py          # Inicialização da API
├── rabbit_worker.py # Worker do RabbitMQ
└── requirements.txt
```

### Organização

- **Controller**: camada de entrada (endpoints)  
- **Services**: regras de negócio  
- **Repository**: acesso a dados  
- **Config**: banco e segurança  
- **Core**: definições centrais (RBAC)  
- **Dependencies**: injeção de dependências  
- **Messaging**: comunicação assíncrona com RabbitMQ  

---

## Autenticação e Autorização

- Autenticação baseada em **JWT (JSON Web Token)**  
- Controle de acesso utilizando **RBAC (Role-Based Access Control)**  

---

## Mensageria

O projeto utiliza **RabbitMQ** para processamento assíncrono nas operações de:

- CRUD de usuários  
- Criação e gerenciamento de diários
- Processos desacoplados da API principal

---

## Infraestrutura com Docker

A aplicação é containerizada utilizando Docker, com separação entre:

- API (FastAPI)  
- Worker (processamento assíncrono)  
- PostgreSQL  
- RabbitMQ  

O ambiente é orquestrado via **Docker Compose**, garantindo consistência entre desenvolvimento e CI.

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:18-alpine
    container_name: pokeDiary_postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  rabbitmq:
    image: rabbitmq:3-management
    container_name: pokeDiary_rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}

  api:
    build: .
    container_name: pokeDiary_api
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      RUN_MIGRATIONS: "true"
    depends_on:
      - postgres
      - rabbitmq
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    restart: always

  worker:
    build: .
    container_name: pokeDiary_worker
    env_file:
      - .env
    environment:
      RUN_MIGRATIONS: "false"
    depends_on:
      - postgres
      - rabbitmq
    command: python rabbit_worker.py
    restart: always

volumes:
  postgres_data:
```

Além disso, o projeto utiliza um **entrypoint customizado** para:

- Executar `prisma generate`
- Aplicar migrations automaticamente com `prisma migrate deploy`

---

## CI/CD com Jenkins

O projeto possui pipeline de integração contínua utilizando Jenkins, com:

- Build automatizado com Docker
- Subida dos serviços via Docker Compose
- Injeção segura de variáveis via credentials
- Geração dinâmica de .env
- Healthcheck da API
- Logs automáticos em caso de falha
- Cleanup completo do ambiente após execução

---

## Etapas do Pipeline

- Checkout do código
- Criação dinâmica de variáveis de ambiente
- Build das imagens Docker
- Subida dos serviços
- Verificação de disponibilidade da API
- Finalização e limpeza do ambiente

---

## Variáveis de Ambiente

Exemplo de configuração:

```env
DATABASE_URL="postgresql://user:password@postgres:5432/postgres"
SECRET_KEY="your_secret_key"

POSTGRES_USER="your_user"
POSTGRES_PASSWORD="your_password"

RABBITMQ_USER="your_user"
RABBITMQ_PASSWORD="your_password"

POKEMON_API_URL="https://pokeapi.co/api/v2/pokemon"
```

⚠️ **Importante:** O arquivo `.env` não deve ser versionado. Utilize o `.env.example` como base e, em ambiente CI/CD, utilize ***injeção via Jenkins credentials***.

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/pokeDiary.git
cd pokeDiary
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

### 3. Subir a aplicação

```bash
make up-d
```

---

## Comandos disponíveis

```bash
make up-d      # sobe todos os serviços
make down      # para os containers
make logs      # exibe logs
make rebuild   # recria ambiente do zero
```

---

## Observações

- O projeto utiliza **Prisma ORM com migrations automatizadas via Docker**
- O arquivo `entrypoint.sh` executa automaticamente:
  - `prisma generate`
  - `prisma migrate deploy`
- Scripts `.sh` utilizam padrão **LF (Unix)** para compatibilidade com Docker/Linux
- O repositório utiliza `.gitattributes` para garantir padronização de line endings

---

## Melhorias Futuras

- Testes automatizados (unitários e integração)
- Coverage e quality gates
- Deploy automatizado (AWS)
- Observabilidade (logs estruturados + métricas)
- Pipeline CD (entrega contínua) 

---

## Objetivo

Este projeto foi desenvolvido como uma **base profissional para demonstrar domínio técnico**, cobrindo:

- Arquitetura backend moderna
- Integração com serviços externos
- Processamento assíncrono
- Containerização e CI/CD
- Boas práticas de engenharia de software 

---

## Autor

Desenvolvido por **Deryck Henrique Albuquerque**