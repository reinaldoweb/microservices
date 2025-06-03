from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    nome: str
    email: EmailStr


class CustomerResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True  # ← ESSA LINHA É ESSENCIAL!