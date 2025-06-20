from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True  # ← ESSA LINHA É ESSENCIAL!