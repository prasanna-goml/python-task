import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.services.ticket_service import update_ticket
from app.schemas.ticket import UpdateTicketRequest


@pytest.mark.asyncio
async def test_update_ticket_success():
    db = AsyncMock()

    ticket = AsyncMock()
    ticket.title = "Old"

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=ticket)
    ):
        data = UpdateTicketRequest(title="New")

        updated = await update_ticket(uuid4(), data, db)

        assert updated.title == "New"

        db.commit.assert_awaited_once()
        db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_multiple_fields():
    db = AsyncMock()

    ticket = AsyncMock()

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=ticket)
    ):
        data = UpdateTicketRequest(
            title="Updated",
            priority="high"
        )

        updated = await update_ticket(uuid4(), data, db)

        assert updated.title == "Updated"
        assert updated.priority == "high"


@pytest.mark.asyncio
async def test_update_ticket_not_found():
    db = AsyncMock()

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=None)
    ):
        result = await update_ticket(
            uuid4(),
            UpdateTicketRequest(title="New"),
            db,
        )

        assert result is None


@pytest.mark.asyncio
async def test_update_commit_failure():
    db = AsyncMock()

    ticket = AsyncMock()

    db.commit.side_effect = Exception("DB Error")

    with patch(
        "app.services.ticket_service.get_ticket",
        AsyncMock(return_value=ticket)
    ):
        with pytest.raises(Exception):
            await update_ticket(
                uuid4(),
                UpdateTicketRequest(title="New"),
                db,
            )