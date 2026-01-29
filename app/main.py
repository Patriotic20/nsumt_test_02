import uvicorn
from core.config import settings
from core.db_helper import db_helper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.admin_auth import AdminAuth
from models.views import register_models
from modules.router import router
from sqladmin import Admin

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
authentication_backend = AdminAuth(secret_key=settings.admin.secret_key)

# Ensure static directory exists
os.makedirs("app/static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
admin = Admin(
    app, engine=db_helper.engine, authentication_backend=authentication_backend
)
register_models(admin)


def main():
    uvicorn.run(
        app=settings.server.app_path,
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
    )


if __name__ == "__main__":
    main()
