from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, Client, engine, get_db
from models import ClientOut, CreateClient, OrderIncrement, UpdateClient

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CarPart Clients API")


@app.post("/clients", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(payload: CreateClient, db: Session = Depends(get_db)):
    """Add a new client."""
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@app.get("/clients", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    """Return every client."""
    return db.query(Client).all()


@app.get("/clients/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Return one client's record."""
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.patch("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, payload: UpdateClient, db: Session = Depends(get_db)):
    """Update a client's name and email."""
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    client.first_name = payload.first_name
    client.last_name = payload.last_name
    client.email = payload.email
    db.commit()
    db.refresh(client)
    return client


@app.post("/clients/{client_id}/orders", response_model=ClientOut)
def add_orders(client_id: int, payload: OrderIncrement, db: Session = Depends(get_db)):
    """Increase a client's order count (used by employees when an order comes in by mail)."""
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    client.order_count += payload.quantity
    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Remove a client."""
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
