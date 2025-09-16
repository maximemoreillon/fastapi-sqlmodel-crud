from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from db import get_session
from typing import Annotated
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


@router.get("/{id}")
def read_hero(id: int, session=Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Hero not found")
    return item


# TODO: Update


@router.delete("/{id}")
def delete_hero(id: int, session=Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
