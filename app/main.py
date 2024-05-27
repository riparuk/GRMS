from fastapi import Depends, FastAPI
from app.db import models
from app.routers import properties, staffs, tasks, messages
from .dependencies import get_query_token, get_token_header
from app.db.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    # dependencies=[Depends(get_query_token)],
    )

app.include_router(messages.router)
app.include_router(properties.router)
app.include_router(staffs.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}