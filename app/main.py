from fastapi import Depends, FastAPI
from app.db import models
from app.routers import properties, staffs, images, requests
from .dependencies import get_query_token, get_token_header
from app.db.database import engine
from app.routers import simulate
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    # dependencies=[Depends(get_query_token)],
    )

app.include_router(images.router)
app.include_router(properties.router)
app.include_router(staffs.router)
app.include_router(requests.router)
app.include_router(simulate.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
