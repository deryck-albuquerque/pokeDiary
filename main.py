import uvicorn
from fastapi import FastAPI

def init_app() -> FastAPI:
    app = FastAPI(
        title="pokeDiary",
        description=(
            "O pokeDiary é uma API backend desenvolvida para gerenciamento de um sistema de diário personalizado de Pokémons. "
            "Construída com FastAPI, a aplicação segue princípios de Clean Architecture, garantindo escalabilidade, "
            "manutenibilidade e separação de responsabilidades. O sistema integra PostgreSQL como banco de dados principal, "
            "RabbitMQ para processamento assíncrono de tarefas e Prisma ORM para modelagem e migrações. "
            "A aplicação é totalmente containerizada com Docker e preparada para ambientes de produção, incluindo pipelines de CI/CD e deploy em cloud."
        ),
        version="1.0.0"
    )

    from app.controller import users, auth, diary
    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(diary.router)

    return app

app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)