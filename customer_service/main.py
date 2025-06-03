from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import Customer
from schemas import CustomerCreate, CustomerResponse

app = FastAPI()


@app.post("/customers", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    # Verifica se já existe cliente com mesmo e-mail
    result = await db.execute(select(Customer).where(Customer.email == customer.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    new_customer = Customer(nome=customer.nome, email=customer.email)
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer


@app.get("/customers", response_model=list[CustomerResponse])
async def list_customers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer))
    return result.scalars().all()


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return customer


@app.delete("/customers/{customer_id}", status_code=204)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    await db.delete(customer)
    await db.commit()
