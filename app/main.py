from fastapi import FastAPI

app = FastAPI(title="E-Shop API")


@app.get("/")
def root():
    return {"message": "E-Shop API is running"}