from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from . import schemas, models
from .db import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items", response_model=list[schemas.Item])
def find_items(
    is_done: str | None = Query(default=None, regex="^(yes|no)$"),
    has_description: str | None = Query(default=None, regex="^(yes|no)$"),
    db: Session = Depends(get_db),
):
    items = db.query(models.Item)

    if is_done is not None:
        items = items.filter(models.Item.is_done == (is_done == "yes"))

    if has_description is not None:
        if has_description == "yes":
            items = items.filter(models.Item.description != "")
        else:
            items = items.filter(models.Item.description == "")

    return items.all()


@app.post("/items", response_model=schemas.Item, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.Item(description=item.description, is_done=item.is_done)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/{item_id}", response_model=schemas.Item)
def find_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if update.description is not None:
        item.description = update.description
    if update.is_done is not None:
        item.is_done = update.is_done

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return Response(status_code=200)
