import pytest
from unittest.mock import MagicMock, AsyncMock

from app.schemas.ticket import CreateTicketRequest
from app.services.ticket_service import create_ticket


@pytest.mark.asyncio
async def test_create_ticket_success():
    db = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    data = CreateTicketRequest(
        title="Login Issue",
        priority="high",
        assignee="Alice"
    )

    ticket = await create_ticket(data, db)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert ticket.title == "Login Issue"
    assert ticket.priority == "high"
    assert ticket.status == "open"
    assert ticket.assignee == "Alice"


@pytest.mark.asyncio
async def test_create_ticket_without_assignee():
    db = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    data = CreateTicketRequest(
        title="Bug Report",
        priority="low",
        assignee=None
    )

    ticket = await create_ticket(data, db)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert ticket.title == "Bug Report"
    assert ticket.priority == "low"
    assert ticket.assignee is None
    assert ticket.status == "open"


@pytest.mark.asyncio
async def test_create_ticket_invalid_title():
    with pytest.raises(Exception):
        CreateTicketRequest(
            title="",
            priority="high",
            assignee="Alice"
        )


@pytest.mark.asyncio
async def test_create_ticket_invalid_priority():
    with pytest.raises(Exception):
        CreateTicketRequest(
            title="Server Down",
            priority="invalid",
            assignee="Alice"
        )


@pytest.mark.asyncio
async def test_create_ticket_commit_failure():
    db = MagicMock()
    db.commit = AsyncMock(side_effect=Exception("DB Error"))
    db.refresh = AsyncMock()

    data = CreateTicketRequest(
        title="Database Issue",
        priority="medium",
        assignee="Bob"
    )

    with pytest.raises(Exception, match="DB Error"):
        await create_ticket(data, db)


@pytest.mark.asyncio
async def test_create_ticket_refresh_failure():
    db = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock(side_effect=Exception("Refresh Error"))

    data = CreateTicketRequest(
        title="Network Issue",
        priority="low",
        assignee="Charlie"
    )

    with pytest.raises(Exception, match="Refresh Error"):
        await create_ticket(data, db)