import uvicorn
from fastapi import FastAPI
from app.config.connection_db import prisma_connection

def init_app():
    app = FastAPI(
        title="pokeDiary",
        description="FastAPI + PostgresSQL + Prisma",
        version="initial"
    )

    @app.on_event("startup")
    async def startup():
        await prisma_connection.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await prisma_connection.disconnect()

    from app.controller import users

    app.include_router(users.router)
    return app

app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)