import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.services.ticket_service import get_ticket


@pytest.mark.asyncio
async def test_get_ticket_found():
    db = MagicMock()
    db.execute = AsyncMock()

    ticket = object()

    result = MagicMock()
    result.scalar_one_or_none.return_value = ticket

    db.execute.return_value = result

    response = await get_ticket(uuid4(), db)

    assert response is ticket


@pytest.mark.asyncio
async def test_get_ticket_another_found():
    db = MagicMock()
    db.execute = AsyncMock()

    ticket = object()

    result = MagicMock()
    result.scalar_one_or_none.return_value = ticket

    db.execute.return_value = result

    response = await get_ticket(uuid4(), db)

    assert response == ticket


@pytest.mark.asyncio
async def test_get_ticket_not_found():
    db = MagicMock()
    db.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = None

    db.execute.return_value = result

    response = await get_ticket(uuid4(), db)

    assert response is None


@pytest.mark.asyncio
async def test_get_ticket_db_failure():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=Exception("DB Error"))

    with pytest.raises(Exception, match="DB Error"):
        await get_ticket(uuid4(), db)