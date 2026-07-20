from uuid import uuid4
from datetime import datetime

from app.models.ticket import Ticket
from app.schemas.ticket import CreateTicketRequest

tickets: list[Ticket] = []

def create_ticket(data: CreateTicketRequest):
    ticket = Ticket(
        id=uuid4(),
        title=data.title,
        priority=data.priority,
        status="open",
        created_at=datetime.now(),
    )

    tickets.append(ticket)

    return ticket

from typing import Optional


def get_all():  
    result = tickets
    return result

def get_ticket(ticket_id: str) -> Ticket | None:
    for ticket in tickets:
        if str(ticket.id) == ticket_id:
            return ticket

    return None

from app.schemas.ticket import UpdateTicketRequest


def update_ticket(
    ticket_id: str,
    data: UpdateTicketRequest,
) -> Ticket | None:

    ticket = get_ticket(ticket_id)

    if ticket is None:
        return None

    updates = data.model_dump(exclude_unset=True)

    if "title" in updates:
        ticket.title = updates["title"]

    if "priority" in updates:
        ticket.priority = updates["priority"]

    if "status" in updates:
        ticket.status = updates["status"]

    return ticket

def delete_ticket(ticket_id: str) -> bool:
    ticket = get_ticket(ticket_id)

    if ticket is None:
        return False

    tickets.remove(ticket)

    return True