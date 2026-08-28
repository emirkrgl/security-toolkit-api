from sqlalchemy import Column,Integer,String,DateTime
from app.core.database import Base
from datetime import datetime,timezone
class ScanResult(Base):
    __tablename__="toolkit"
    id=Column(Integer,primary_key=True,index=True)
    task_id=Column(String,nullable=False)
    tool=Column(String,nullable=False)
    target=Column(String)
    status=Column(String,nullable=False)
    result=Column(String)
    created_at=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)