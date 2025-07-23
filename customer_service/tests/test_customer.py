import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from customer_service.crud import atualizar_cliente, buscar_cliente
from ..schemas import ClienteResponse, ClienteUpdate
from ..main import create_cliente
from ..models import Cliente, ClienteCreate


# Uma fixture para criar uma instância de AsyncMock
# para a sessão do banco de dados
@pytest.fixture
def mock_db_session():
    db_session = AsyncMock()
    # Mock para o metodo execute
    db_session.execute.return_value = AsyncMock()
    # scalar_one_or_none de ser um AsyncMock
    db_session.execute.return_value.scalar_one_or_none.return_value = None
    # Mocks para os outros métodos que não retornam valor específico
    db_session.add = MagicMock()
    db_session.commit = AsyncMock()
    db_session.refresh = AsyncMock()
    return db_session


# --- Teste com sucesso ---
@pytest.mark.asyncio
async def test_create_cliente_com_sucesso(mock_db_session):
    # Dados do cliente a ser criado
    cliente_data = ClienteCreate(nome="Teste", email="teste@example.com")
    # chama a função
    novo_cliente = await create_cliente(
        db=mock_db_session, cliente=cliente_data)
    mock_db_session.execute.assert_called_once()
    mock_db_session.execute.return_value.scalar_one_or_none.assert_called_once()
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()

    assert novo_cliente.nome == "Teste"
    assert novo_cliente.email == "teste@example.com"
    assert isinstance(novo_cliente, Cliente)


# --- Teste de Cliente Existente ---
@pytest.mark.asyncio
async def test_criar_cliente_existente(mock_db_session):
    """
    Testa se a função criar_cliente levanta HTTPException
    quando o cliente com o mesmo email já existe.
    """
    # Dados do cliente a ser criado
    cliente_data = ClienteCreate(
        nome="Existente", email="existente@example.com")

    # Configura o mock para simular que o cliente já existe
    # Cria uma instância de Cliente para ser o cliente_existente
    cliente_mock_existente = ClienteCreate(
        id=1, nome="Existente", email="existente@example.com"
    )
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
        cliente_mock_existente
    )

    with pytest.raises(HTTPException) as exc_info:
        # O mock_db_session deve ser o primeiro argumento passado
        # Use argumentos nomeados para clareza
        await create_cliente(db=mock_db_session, cliente=cliente_data)

    # Asserts para verificar a exceção e o comportamento:
    # 1. A exceção é do tipo HTTPException
    assert exc_info.type == HTTPException
    # 2. O código de status da exceção é 400
    assert exc_info.value.status_code == 400
    # 3. A mensagem de detalhe é a esperada
    assert exc_info.value.detail == (
        "Já existe um cliente cadastrado com este e-mail.")
    # 4. commit e add NÃO foram chamados (porque o cliente já existia)
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()


@pytest.mark.asyncio
async def test_atualizar_cliente_sucesso():
    # Simulando o cliente retornado pela função buscar_cliente
    cliente_fake = MagicMock(spec=Cliente)
    cliente_fake.nome = "Antigo Nome"

    # simular dados atualizados
    dados = ClienteUpdate(nome="Novo Nome")

    # Mock da sessao do banco
    db_mock = AsyncMock()

    # Pasta na função buscar_cliente que está
    # 1sendo chamada dentro de atualizar_cliente
    with patch(
                "customer_service.crud.buscar_cliente",
                return_value=cliente_fake
                ):
        resultado = await atualizar_cliente(db=db_mock, id=1, dados=dados)

        # Verifica se os dados forma atulizados
        assert resultado.nome == "Novo Nome"

        # Verifica se os metodos do banco foram chamados
        db_mock.commit.assert_awaited_once()
        db_mock.refresh.assert_called_once_with(cliente_fake)


@pytest.mark.asyncio
async def test_atualizar_cliente_nao_encontrado():
    db_mock = AsyncMock()
    with patch(
                "customer_service.crud.buscar_cliente", new_callable=AsyncMock
                ) as mock_buscar:
        mock_buscar.return_value = None
        resultado = await atualizar_cliente(
            db=db_mock, id=999, dados=ClienteUpdate(nome="Teste"))
        assert resultado is None
        db_mock.commit.assert_not_called()


@pytest.mark.asyncio
async def test_atualizar_cliente_multiplos_campos():
    cliente_fake = MagicMock(spec=Cliente)
    db_mock = AsyncMock()
    dados = ClienteUpdate(nome="Teste", email="teste@email.com")

    with patch("customer_service.crud.buscar_cliente",
               return_value=cliente_fake
               ):
        resultado = await atualizar_cliente(db=db_mock, id=1, dados=dados)
        assert resultado.nome == "Teste"
        assert resultado.email == "teste@email.com"
        db_mock.commit.assert_awaited_once()


   