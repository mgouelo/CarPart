from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    quantity: int = Field(default=0, ge=0)

class UpdateProduct(BaseModel):
    description: str = Field(min_length=1)

class RevisedQuantity(BaseModel):
    quantity: int = Field(gt=0, description="Number of units to add or remove")

class ProductOut(BaseModel):
    id: str
    name: str
    description: str
    quantity: int