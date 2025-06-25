from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteResponse, ClienteUpdate


router = APIRouter()


@router.post("/", response_model=ClienteResponse, status_code=200)
async def create_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(
                        get_db)
):
    # Verifica se já existe cliente com mesmo e-mail
    result = await db.execute(
        select(Cliente).where(Cliente.email == cliente.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_cliente = Cliente(nome=cliente.nome, email=cliente.email)
    db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    return novo_cliente


# @router.get("/clientes", response_model=list[ClienteResponse])
# async def list_clientes(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Cliente))
#     return result.scalars().all()


# @router.get("/clientes/{cliente_id}", response_model=ClienteResponse)
# async def obter_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
#     cliente = result.scalar_one_or_none()
#     if not cliente:
#         raise HTTPException(status_code=404, detail="Cliente não encontrado")
#     return cliente


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_customer(cliente_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = result.scalar_one_or_none()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente


@router.patch("/{id}", response_model=ClienteResponse)
async def update_cliente(
    id: int, cliente_dados: ClienteUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Cliente).where(Cliente.id == id))
    cliente = result.scalar_one_or_none()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Garante que apenas os campos que forma passados serão atualizados
    cliente_atualizado = cliente_dados.model_dump(exclude_unset=True)
    for Field, value in cliente_atualizado.items():
        setattr(cliente, Field, value)

    await db.commit()
    await db.refresh(cliente)
    return cliente


@router.delete("/{id}", status_code=204)
async def delete_cliente(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == id))
    cliente = result.scalar_one_or_none()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    await db.delete(cliente)
    await db.commit()
    return {"detail": "Cliente deletado com sucesso"}
