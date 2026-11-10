
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.database import get_db
from app.db.models.user import User
from app.db.models.category import Category
from app.db.models.product import Product
from app.core.security import create_access_token


@pytest.fixture
def admin_headers(client):
    db = next(app.dependency_overrides[get_db]())

    admin = User(
        email="admin@test.com",
        password_hash="test_hash",
        role="admin",
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = create_access_token(subject=str(admin.id))
    db.close()

    return {"Authorization": f"Bearer {token}"}

