from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    task_id: str