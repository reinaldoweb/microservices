from typing import Optional
from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True