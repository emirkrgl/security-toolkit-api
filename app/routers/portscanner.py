from fastapi import APIRouter,BackgroundTasks,Depends
from app.services.portscanner import run
from app.models.portscanner import PortScanRequest
import uuid
from app.core.database import get_db
from app.models.db_models import ScanResult
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
import json
router=APIRouter()
@router.get("/scan/status/{task_id}")

def get_status(task_id:str,db:Session=Depends(get_db)):
   a=db.query(ScanResult).filter(ScanResult.task_id==task_id).first()
   if a:
      return {"status":a.status,"result":json.loads(a.result) if a.result else None}
   else:
      return {"error":"Bu task_id ile eşleşen bir işlem bulunamadı."}
   
def run_and_store(task_id, target, start_port, end_port):
   db=SessionLocal()
   a=db.query(ScanResult).filter(ScanResult.task_id == task_id).first()
   a.status="done"
   a.result=json.dumps(run(target, start_port, end_port))
   db.commit()
   db.close()

@router.post("/scan/port")
def scan_port(request:PortScanRequest,background_task:BackgroundTasks,db:Session=Depends(get_db)):
   
   task_id=str(uuid.uuid4())
   yeni_nesne=ScanResult(task_id=task_id, tool="port_scanner", target=request.target, status="running", result=None)
   db.add(yeni_nesne)
   db.commit()
   background_task.add_task(run_and_store,task_id,request.target,request.start_port,request.end_port)
   return {"task_id": task_id}
