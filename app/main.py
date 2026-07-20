from fastapi import FastAPI
from app.api.tickets import router

app = FastAPI(title="AI Service Desk")

app.include_router(router)