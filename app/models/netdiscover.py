from pydantic import BaseModel

class NetDiscoverRequest(BaseModel):
    target_network:str