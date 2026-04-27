import uvicorn
from fastapi import FastAPI

def init_app() -> FastAPI:
    app = FastAPI(
        title="pokeDiary",
        description="FastAPI + PostgreSQL",
        version="initial"
    )

    from app.controller import users, auth, diary
    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(diary.router)

    return app

app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)