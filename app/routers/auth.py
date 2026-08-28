from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import User
from app.models.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token
from app.models.db_models import BlacklistedToken
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import oauth2_scheme

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
def login_user(
    request: OAuth2PasswordRequestForm = Depends(), # Hatanın çözümü tam olarak bu satır!
    db: Session = Depends(get_db)
):
    # Kullanıcıyı bul
    user = db.query(User).filter(User.username == request.username).first()
    
    # Kullanıcı yoksa veya şifre yanlışsa
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )
    
    # Şifre doğruysa token üret
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/logout")
def logout_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    already_blacklisted = db.query(BlacklistedToken).filter(BlacklistedToken.token == token).first()
    
    if already_blacklisted:
        raise HTTPException(status_code=400, detail="Token is already logged out.")
    
    
    blacklisted_token = BlacklistedToken(token=token)
    db.add(blacklisted_token)
    db.commit()
    
    return {"message": "User logged out successfully."}