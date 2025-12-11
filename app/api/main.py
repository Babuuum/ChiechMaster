from fastapi import FastAPI
from .routers.user import router as user_router

app = FastAPI(title='Chiech_Master')

app.include_router(user_router)

