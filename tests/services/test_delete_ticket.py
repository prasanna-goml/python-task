import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.services.ticket_service import delete_ticket


@pytest.mark.asyncio
async def test_delete_ticket_success():
    db = AsyncMock()

    ticket = AsyncMock()

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=ticket)
    ):
        result = await delete_ticket(uuid4(), db)

        assert result is True

        db.delete.assert_awaited_once_with(ticket)
        db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_second_ticket():
    db = AsyncMock()

    ticket = AsyncMock()

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=ticket)
    ):
        assert await delete_ticket(uuid4(), db) is True


@pytest.mark.asyncio
async def test_delete_ticket_not_found():
    db = AsyncMock()

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=None)
    ):
        result = await delete_ticket(uuid4(), db)

        assert result is False


@pytest.mark.asyncio
async def test_delete_db_failure():
    db = AsyncMock()

    ticket = AsyncMock()

    db.delete.side_effect = Exception("DB Error")

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=ticket)
    ):
        with pytest.raises(Exception):
            await delete_ticket(uuid4(), db)