from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db.database import get_db
from pwdlib import PasswordHash
from app.db.models.user import User
from app.schemas.user import UserCreate, UserResponse

app = FastAPI(title="E-Shop API")
password_hash = PasswordHash.recommended()

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = password_hash.hash(user_data.password)
    
    # Create the user instance
    user = User(email=user_data.email, 
                password_hash=hashed_password
                )
    
    # Add the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@app.get("/")
def root():
    return {"message": "E-Shop API is running"}

@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users