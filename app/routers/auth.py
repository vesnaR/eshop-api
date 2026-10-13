from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.user import LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])
password_hash = PasswordHash.recommended()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
    ):
    
    user = db.query(User).filter(
        User.email == login_data.email
        ).first()

    if user is None or not password_hash.verify(
        login_data.password, 
        user.password_hash
        ):
        
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
            )

    token = create_access_token(subject=str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer",
    }