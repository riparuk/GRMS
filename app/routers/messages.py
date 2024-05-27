from fastapi import APIRouter, Depends, HTTPException
from pydantic.v1 import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.db import crud, schemas

from ..dependencies import get_db, get_token_header

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def is_request(message: str):
    
    if "need" in message:
        is_request = True
    else:
        is_request = False
    
    return {"is_request": is_request}
