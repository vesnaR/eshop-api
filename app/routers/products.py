from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import require_admin
from app.schemas.pagination import PaginatedResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from math import ceil
from app.db.models.product import Product
from app.db.models.category import Category
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])



@router.get("/", response_model=PaginatedResponse[ProductResponse])
def get_products(
    search: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: str=Query(default="id", pattern="^(id|name|price)$"),
    order: str=Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
   
):
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    total = query.count()

    
    sort_column = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price,
    }[sort_by]

    if order == "desc":
        query = query.order_by(sort_column.desc(), Product.id.asc())
    else:
        query = query.order_by(sort_column.asc(), Product.id.asc())

    products = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


    pages = ceil(total / limit) if total > 0 else 0

    return {
        "items": products,
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": pages,
    }



@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    return product


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found.",
        )

    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    update_data = product_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.id == update_data["category_id"]
        ).first()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found.",
            )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    db.delete(product)
    db.commit()

    return