from fastapi import FastAPI
from app.routers.portscanner import router
app = FastAPI()
app.include_router(router)
