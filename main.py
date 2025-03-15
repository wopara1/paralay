from fastapi import FastAPI
from .routes import router
app = FastAPI()

# Include your microservice with the proper route prefix.
app.include_router(router)

# Main app url
@app.get("/")
def read_root():
    return {"Hello": "W Parlay App"}