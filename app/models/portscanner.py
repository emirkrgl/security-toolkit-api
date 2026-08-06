from pydantic import BaseModel,Field
class PortScanRequest(BaseModel):
    target:str
    start_port:int=Field(gt=0,le=65535)
    end_port:int=Field(gt=0,le=65535)