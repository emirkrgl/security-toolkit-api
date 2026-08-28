from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import User
from app.models.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token
router=APIRouter()
@router.post("/auth/register")
def register_user(request:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.username==request.username).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists.")
    hashed_pwd=hash_password(request.password)
    new_user=User(username=request.username,hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created successfully."}
@router.post("/auth/login")
def login_user(request:UserCreate,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==request.username).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid username or password.")
    if user:
        if verify_password(request.password,user.hashed_password)==False:
            raise HTTPException(status_code=401,detail="Invalid username or password.")
        else:
            token=create_access_token({"sub": user.username})
            return {"access_token": token, "token_type": "bearer"}