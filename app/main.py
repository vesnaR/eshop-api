
from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

app = FastAPI(title="E-Shop API")

app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "E-Shop API is running"}

