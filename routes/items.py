from fastapi import APIRouter, Depends, HTTPException, status, Response
from db import get_session

# from db import Item
from models.item import Item

router = APIRouter(prefix="/items")


@router.post("/")
def create_hero(item: Item, session=Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/")
async def handle(session=Depends(get_session)):
    items = session.query(Item).all()
    return {"items": items}
