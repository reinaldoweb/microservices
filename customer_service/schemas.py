from typing import Optional
from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True