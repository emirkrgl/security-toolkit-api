from fastapi import APIRouter,BackgroundTasks,Depends
from app.core.security import get_current_user
from app.services.netdiscover import run
from app.models.netdiscover import NetDiscoverRequest
import uuid
from app.core.database import get_db
from app.models.db_models import ScanResult
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
import json
from app.core.security import get_current_user
router=APIRouter()

@router.get("/scan/netdiscover/status/{task_id}")
def get_status_network(task_id:str,db:Session=Depends(get_db)):
    a=db.query(ScanResult).filter(ScanResult.task_id==task_id).first()
    if a:
        return {"status":a.status,"result":json.loads(a.result) if a.result else None}
    else:
        return {"error":"Bu task_id ile eşleşen bir işlem bulunamadı."}
    
    
def run_and_store(task_id,target_network):
    db=SessionLocal()
    a=db.query(ScanResult).filter(ScanResult.task_id==task_id).first()
    a.status="done"
    a.result=json.dumps(run(target_network))
    db.commit()
    db.close()

@router.post("/scan/netdiscover")
def scan_netdiscover(request:NetDiscoverRequest,background_tasks:BackgroundTasks,db:Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    task_id=str(uuid.uuid4())
    yeninesne=ScanResult(task_id=task_id, tool="netdiscover", target=request.target_network, status="running", result=None)
    db.add(yeninesne)
    db.commit()
    background_tasks.add_task(run_and_store,task_id,request.target_network)
    return {"task_id": task_id}