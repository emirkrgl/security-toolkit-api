from fastapi import FastAPI
from app.routers.portscanner import router
from app.routers.netdiscover import router as netdiscover_router
from app.routers.ai_analyzer import router as ai_analyzer_router
from app.routers.auth import router as auth_router
app = FastAPI()
app.include_router(router)
app.include_router(netdiscover_router)
app.include_router(ai_analyzer_router)
app.include_router(auth_router)
