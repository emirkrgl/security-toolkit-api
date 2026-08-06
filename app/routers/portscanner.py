from fastapi import APIRouter
from app.services.portscanner import run
from app.models.portscanner import PortScanRequest
router=APIRouter()
@router.post("/scan/port")
def scan_port(request:PortScanRequest):
    sonuc=run(request.target,request.start_port,request.end_port)
    return sonuc
