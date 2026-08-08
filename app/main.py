from fastapi import FastAPI
from app.routers.portscanner import router
from app.routers.netdiscover import router as netdiscover_router
app = FastAPI()
app.include_router(router)
app.include_router(netdiscover_router)