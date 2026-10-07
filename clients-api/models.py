from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CreateClient(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    order_count: int = Field(default=0, ge=0)

class UpdateClient(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr

class OrderIncrement(BaseModel):
    quantity: int = Field(gt=0, description="Number of new orders to add to the client's count")

class ClientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    order_count: int
