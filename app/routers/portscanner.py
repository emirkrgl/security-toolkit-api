from fastapi import APIRouter,BackgroundTasks
from app.services.portscanner import run
from app.models.portscanner import PortScanRequest
import uuid
router=APIRouter()
tasks={}
@router.get("/scan/status/{task_id}")
def get_status(task_id:str):
   if task_id in tasks:
        return tasks[task_id] 
   else:
        return {"error": "Bu task_id ile eşleşen bir işlem bulunamadı."}
def run_and_store(task_id, target, start_port, end_port):
   a=run(target, start_port, end_port)
   tasks[task_id]={"status": "done", "result":a}
@router.post("/scan/port")
def scan_port(request:PortScanRequest,background_task:BackgroundTasks):
   task_id=str(uuid.uuid4())
   tasks[task_id]={
      "status":"running",
      "result":None
   }
   background_task.add_task(run_and_store,task_id,request.target,request.start_port,request.end_port)
   return {"task_id": task_id}
