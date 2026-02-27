import uvicorn
from fastapi import FastAPI
from mangum import Mangum

def init_app() -> FastAPI:
    app = FastAPI(
        title="pokeDiary",
        description="FastAPI + PostgresSQL + Prisma",
        version="initial"
    )

    from app.controller import users
    app.include_router(users.router)

    return app

app = init_app()
handler = Mangum(app)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)