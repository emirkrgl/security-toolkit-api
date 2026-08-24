import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ai_analyzer import run
from app.models.ai_analyzer import AnalyzeRequest
from app.models.db_models import ScanResult 
router = APIRouter()
@router.post("/scan/analyze")
def analyze_scan(request: AnalyzeRequest, db: Session = Depends(get_db)):
    a = db.query(ScanResult).filter(ScanResult.task_id == request.task_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        if a.status != "done":
            raise HTTPException(status_code=400, detail="Task is not completed yet")
        else:
            analysis_result = run(json.loads(a.result))
            return {"analysis_result": analysis_result}
