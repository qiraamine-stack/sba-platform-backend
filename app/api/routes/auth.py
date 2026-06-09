from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db, Base, engine
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

Base.metadata.create_all(bind=engine)
router = APIRouter()

class RegisterInput(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "buyer"

class LoginInput(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterInput, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"token": token, "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}}

@router.post("/login")
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"token": token, "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}}

@router.get("/me")
def get_me(db: Session = Depends(get_db)):
    return {"message": "Auth working"}
