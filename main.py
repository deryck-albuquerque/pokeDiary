import uvicorn
from fastapi import FastAPI

def init_app() -> FastAPI:
    app = FastAPI(
        title="pokeDiary",
        description="FastAPI + PostgresSQL + Prisma",
        version="initial"
    )

    from app.controller import users, auth
    app.include_router(users.router)
    app.include_router(auth.router)

    return app

app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)