from fastapi import APIRouter
from app.services.netdiscover import run
from app.models.netdiscover import NetDiscoverRequest
router=APIRouter()
@router.post("/scan/netdiscover")
def scan_netdiscover(request:NetDiscoverRequest):
    sonuc=run(request.target_network)
    return sonuc