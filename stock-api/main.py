from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException, status

from database import products
from models import CreateProduct, ProductOut, RevisedQuantity, UpdateProduct

app = FastAPI(title="CarPart Stock API")


def to_object_id(product_id: str) -> ObjectId:
    """Convert a string id from the URL into a Mongo ObjectId, or raise 404."""
    try:
        return ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Product not found")


def serialize(document: dict) -> dict:
    """Turn a Mongo document into a dict matching the ProductOut model."""
    return {
        "id": str(document["_id"]),
        "name": document["name"],
        "description": document["description"],
        "quantity": document["quantity"],
    }


@app.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: CreateProduct):
    """Add a new product to the stock."""
    result = products.insert_one(payload.model_dump())
    document = products.find_one({"_id": result.inserted_id})
    return serialize(document)


@app.get("/products", response_model=list[ProductOut])
def list_products():
    """Return every product in the stock."""
    return [serialize(doc) for doc in products.find()]


@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: str):
    """Return one product: its description and remaining quantity."""
    document = products.find_one({"_id": to_object_id(product_id)})
    if document is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize(document)


@app.patch("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: str, payload: UpdateProduct):
    """Update a product's description."""
    object_id = to_object_id(product_id)
    result = products.update_one(
        {"_id": object_id},
        {"$set": {"description": payload.description}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    document = products.find_one({"_id": object_id})
    return serialize(document)


@app.post("/products/{product_id}/add-stock", response_model=ProductOut)
def add_stock(product_id: str, payload: RevisedQuantity):
    """Increase a product's quantity."""
    object_id = to_object_id(product_id)
    result = products.update_one(
        {"_id": object_id},
        {"$inc": {"quantity": payload.quantity}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    document = products.find_one({"_id": object_id})
    return serialize(document)


@app.post("/products/{product_id}/remove-stock", response_model=ProductOut)
def remove_stock(product_id: str, payload: RevisedQuantity):
    """Decrease a product's quantity (cannot go below 0)."""
    object_id = to_object_id(product_id)
    document = products.find_one({"_id": object_id})
    if document is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if payload.quantity > document["quantity"]:
        raise HTTPException(status_code=400, detail="Not enough stock")
    products.update_one({"_id": object_id}, {"$inc": {"quantity": -payload.quantity}})
    document = products.find_one({"_id": object_id})
    return serialize(document)


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    """Remove a product from the stock."""
    result = products.delete_one({"_id": to_object_id(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
