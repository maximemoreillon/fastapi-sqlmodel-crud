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
def read_item(id: int, session=Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{id}")
def update_item(id: int, item: Item, session=Depends(get_session)):
    currentItem = session.get(Item, id)
    if not currentItem:
        raise HTTPException(status_code=404, detail="Item not found")
    data = item.model_dump(exclude_unset=True)
    currentItem.sqlmodel_update(data)
    session.add(currentItem)
    session.commit()
    session.refresh(currentItem)
    return currentItem


@router.delete("/{id}")
def delete_item(id: int, session=Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
