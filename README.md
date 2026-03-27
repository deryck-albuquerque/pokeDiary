# 🐾 pokeDiary

API desenvolvida com **FastAPI** para criação de um diário de Pokémons, consumindo dados da [PokéAPI](https://pokeapi.co) e permitindo que usuários registrem, organizem e gerenciem suas experiências com diferentes Pokémons.

---

## 📌 Sobre o Projeto

O **pokeDiary** é um projeto de estudo focado em boas práticas de desenvolvimento backend, arquitetura de APIs e integração com serviços externos.

A aplicação permite que usuários:

* Criem e gerenciem suas contas
* Registrem Pokémons em um diário personalizado
* Consultem informações detalhadas consumidas da PokéAPI
* Atualizem e removam registros do diário

---

## 🚀 Tecnologias Utilizadas

* **Python**
* **FastAPI**
* **PostgreSQL**
* **Prisma ORM**
* **RabbitMQ** (processamento assíncrono)
* **Docker Compose** (infraestrutura local)

---

## 🧱 Arquitetura do Projeto

O projeto segue uma arquitetura em camadas bem definida, baseada em princípios de **Clean Architecture**, garantindo separação de responsabilidades, baixo acoplamento e alta manutenibilidade.

```bash id="nrmjhp"
pokeDiary/
│
├── controllers/     # Rotas da API (camada de entrada)
├── core/            # Definições centrais (ex: roles de usuário)
├── dependencies/    # Injeções de dependência (auth, etc)
│
├── config/          # Configurações da aplicação
│   ├── connection_db.py  # Conexão com banco de dados
│   └── security.py       # Configuração de autenticação e segurança
│
├── models/          # Modelos de domínio (User, Diary)
├── prisma/          # Schema e client Prisma
├── repositories/    # Acesso aos dados (camada de persistência)
├── services/        # Regras de negócio
├── schemas/         # Schemas (validação e resposta)
│
├── main.py          # Inicialização da API
├── rabbit_worker.py # Worker do RabbitMQ
└── requirements.txt
```

### 🔍 Organização

* **Controllers**: responsáveis por expor os endpoints da API
* **Services**: contêm a lógica de negócio
* **Repositories**: fazem a comunicação com o banco de dados
* **Config**: centraliza conexões e segurança (DB + autenticação)
* **Core**: definições centrais como papéis de usuário (RBAC)
* **Dependencies**: gerenciamento de autenticação e injeções

---

## 🔐 Autenticação e Autorização

* Sistema de autenticação baseado em token
* Controle de acesso utilizando **RBAC (Role-Based Access Control)**

---

## ⚙️ Mensageria (RabbitMQ)

O projeto utiliza **RabbitMQ** para processamento assíncrono nas operações:

* CRUD de usuários
* Criação de diário
* Atualização de diário
* Exclusão de diário

---

## 🐳 Infraestrutura com Docker

O projeto utiliza **Docker Compose** exclusivamente para provisionar os serviços de infraestrutura necessários ao funcionamento da aplicação:

* PostgreSQL (banco de dados)
* RabbitMQ (mensageria)

A aplicação **não é containerizada neste momento** e deve ser executada localmente.

```yaml id="o6n41f"
version: "3"

services:
  postgres:
    image: postgres:18-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
```

📌 **Observação:** futuramente será adicionado suporte à containerização da aplicação com Docker.

---

## 🔑 Variáveis de Ambiente

Exemplo de configuração (`.env`):

```env id="0h6c7x"
DATABASE_URL="postgresql://user:password@localhost:5432/postgres"
SECRET_KEY="your_secret_key"

POSTGRES_USER="your_user"
POSTGRES_PASSWORD="your_password"

RABBITMQ_USER="your_user"
RABBITMQ_PASSWORD="your_password"

POKEMON_API_URL="https://pokeapi.co/api/v2/pokemon"
```

⚠️ **Importante:** Nunca versionar o arquivo `.env`. Utilize um `.env.example`.

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

```bash id="78d1aq"
git clone https://github.com/seu-usuario/pokeDiary.git
cd pokeDiary
```

### 2. Subir os serviços (infraestrutura)

```bash id="td1ps9"
docker-compose up -d
```

### 3. Instalar dependências

```bash id="g8gt2m"
pip install -r requirements.txt
```

### 4. Rodar a API

```bash id="q1sl2g"
python main.py
```

### 5. Rodar o worker do RabbitMQ

```bash id="m2s0tt"
python rabbit_worker.py
```

---

## 📌 Melhorias Futuras

* [ ] Dockerfile para a aplicação
* [ ] Pipeline CI/CD com Jenkins
* [ ] Makefile para automação
* [ ] Testes automatizados
* [ ] Deploy em cloud

---

## 📚 Objetivo

Este projeto foi desenvolvido com foco em:

* Prática de arquitetura backend
* Integração com APIs externas
* Uso de mensageria com RabbitMQ
* Organização de código em camadas
* Aplicação de princípios de Clean Architecture

---

## 👨‍💻 Autor

Desenvolvido por **Deryck Henrique**
