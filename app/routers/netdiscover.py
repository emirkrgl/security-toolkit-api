from fastapi import APIRouter,BackgroundTasks
from app.services.netdiscover import run
from app.models.netdiscover import NetDiscoverRequest
import uuid
router=APIRouter()
tasks={}
@router.get("/scan/netdiscover/status/{task_id}")
def get_status_network(task_id:str):
    if task_id in tasks:
        return tasks[task_id] 
    else:
        return {"error": "Bu task_id ile eşleşen bir işlem bulunamadı."}
def run_and_store(task_id,target_network):
    a=run(target_network)
    tasks[task_id]={"status": "done", "result":a}
@router.post("/scan/netdiscover")
def scan_netdiscover(request:NetDiscoverRequest,background_tasks:BackgroundTasks):
    task_id=str(uuid.uuid4())
    tasks[task_id]={
          "status":"running",
          "result":None
       }
    background_tasks.add_task(run_and_store,task_id,request.target_network)
    return {"task_id": task_id}