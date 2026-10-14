
from fastapi import FastAPI

from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router

app = FastAPI(title="E-Shop API")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(categories_router)


@app.get("/")
def root():
    return {"message": "E-Shop API is running"}

