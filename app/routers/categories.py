from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryWithProducts

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryWithProducts])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category_data: CategoryCreate, 
    db: Session = Depends(get_db)
    ):

    category= Category(
        name=category_data.name,
        description=category_data.description
    )

    db.add(category)

    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A category with this name already exists.",
        )


    return category