from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require_admin
from app.db.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryWithProducts, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryWithProducts])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category_data: CategoryCreate, 
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
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


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found.",
        )

    update_data = category_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update.",
        )

    if "name" in update_data and update_data["name"] is None:
        raise HTTPException(
            status_code=422,
            detail="Category name cannot be null.",
        )

    if "name" in update_data:
        existing_category = db.query(Category).filter(
            Category.name == update_data["name"],
            Category.id != category_id,
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=409,
                detail="A category with this name already exists.",
            )

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found.",
        )

    if category.products:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a category that has products.",
        )

    db.delete(category)
    db.commit()

    return

