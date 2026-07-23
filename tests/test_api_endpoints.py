import pytest
from unittest.mock import AsyncMock, patch


@patch("app.api.tickets.ticket_service.create_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_create_ticket(mock_create, client):
    mock_create.return_value = {
        "id": "0f9d5d7b-59ec-4e52-a65b-6e26d1d9e123",
        "title": "Laptop issue",
        "priority": "high",
        "assignee": "prasanna",
        "status": "open",
        "created_at": "2026-07-22T10:00:00Z",
    }

    response = await client.post(
        "/tickets",
        json={
            "title": "Laptop issue",
            "priority": "high",
            "assignee": "prasanna",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Laptop issue"


@patch("app.api.tickets.ticket_service.get_all", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_all_tickets(mock_get, client):
    mock_get.return_value = [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "title": "Issue 1",
            "priority": "high",
            "assignee": "John",
            "status": "open",
            "created_at": "2026-07-22T10:00:00Z",
        },
        {
    "id": "22222222-2222-2222-2222-222222222222",
    "title": "Issue 2",
    "priority": "low",
    "assignee": "Alice",
    "status": "resolved",
    "created_at": "2026-07-22T11:00:00Z"
},
    ]

    response = await client.get("/tickets")

    assert response.status_code == 200
    assert len(response.json()) == 2


@patch("app.api.tickets.ticket_service.get_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_ticket(mock_get, client):
    ticket_id = "11111111-1111-1111-1111-111111111111"

    mock_get.return_value = {
        "id": ticket_id,
        "title": "Printer issue",
        "priority": "medium",
        "assignee": "Bob",
        "status": "open",
        "created_at": "2026-07-22T10:00:00Z",
    }

    response = await client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Printer issue"


@patch("app.api.tickets.ticket_service.get_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_ticket_not_found(mock_get, client):
    ticket_id = "11111111-1111-1111-1111-111111111111"

    mock_get.return_value = None

    response = await client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 404


@patch("app.api.tickets.ticket_service.update_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_update_ticket(mock_update, client):
    ticket_id = "11111111-1111-1111-1111-111111111111"

    mock_update.return_value = {
        "id": ticket_id,
        "title": "Updated Title",
        "priority": "high",
        "assignee": "prasanna",
        "status": "open",
        "created_at": "2026-07-22T10:00:00Z",
    }

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title": "Updated Title",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


@patch("app.api.tickets.ticket_service.delete_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_delete_ticket(mock_delete, client):
    ticket_id = "11111111-1111-1111-1111-111111111111"

    mock_delete.return_value = True

    response = await client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Ticket deleted successfully"
    }


@patch("app.api.tickets.ticket_service.delete_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_delete_ticket_not_found(mock_delete, client):
    ticket_id = "11111111-1111-1111-1111-111111111111"

    mock_delete.return_value = False

    response = await client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 404

    
@patch("app.api.tickets.ticket_service.update_ticket", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_update_ticket_not_found(mock_update, client):
    ticket_id = "11111111-1111-1111-1111-111111111111"

    mock_update.return_value = None

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={"title": "Updated"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_ticket_missing_title(client):
    response = await client.post(
        "/tickets",
        json={
            "priority": "high",
            "assignee": "prasanna",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_priority(client):
    response = await client.post(
        "/tickets",
        json={
            "title": "Laptop issue",
            "priority": "urgent",
            "assignee": "prasanna",
        },
    )

    assert response.status_code == 422


@patch("app.api.tickets.ticket_service.get_all", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_all_empty(mock_get, client):
    mock_get.return_value = []

    response = await client.get("/tickets")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_invalid_ticket_id(client):
    response = await client.get("/tickets/invalid-id")

    assert response.status_code == 422









