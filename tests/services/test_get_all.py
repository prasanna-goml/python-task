import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.ticket_service import get_all


@pytest.mark.asyncio
async def test_get_all_multiple():
    db = MagicMock()
    db.execute = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = [1, 2]

    db.execute.return_value = result

    tickets = await get_all(db)

    assert len(tickets) == 2
    assert tickets == [1, 2]


@pytest.mark.asyncio
async def test_get_all_single():
    db = MagicMock()
    db.execute = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = [1]

    db.execute.return_value = result

    tickets = await get_all(db)

    assert len(tickets) == 1
    assert tickets == [1]


@pytest.mark.asyncio
async def test_get_all_empty():
    db = MagicMock()
    db.execute = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = []

    db.execute.return_value = result

    tickets = await get_all(db)

    assert tickets == []


@pytest.mark.asyncio
async def test_get_all_db_failure():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=Exception("DB Error"))

    with pytest.raises(Exception, match="DB Error"):
        await get_all(db)