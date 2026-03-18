from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="US Census Chat Agent")

app.include_router(router, prefix="/api")