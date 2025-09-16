from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from db import get_session
from typing import Annotated
from sqlmodel import select

# from db import Item
from models.item import Item

router = APIRouter(prefix="/items")


@router.post("/")
def create_item(item: Item, session=Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/")
async def read_items(
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    session=Depends(get_session),
):
    statement = select(Item).offset(offset).limit(limit)
    items = session.exec(statement).all()
    return {"items": items, "limit": limit, "offset": offset}
