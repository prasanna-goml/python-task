from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.repositories import ticket_repository
from app.schemas.ticket import CreateTicketRequest, UpdateTicketRequest


async def create_ticket(
    data: CreateTicketRequest,
    db: AsyncSession,
):
    ticket = Ticket(
        title=data.title,
        priority=data.priority,
        status="open",
        assignee=data.assignee,
    )

    return await ticket_repository.create(ticket, db)


async def get_all(db: AsyncSession):
    return await ticket_repository.get_all(db)


async def get_ticket(
    ticket_id: UUID,
    db: AsyncSession,
):
    return await ticket_repository.get_by_id(ticket_id, db)


async def update_ticket(
    ticket_id: UUID,
    data: UpdateTicketRequest,
    db: AsyncSession,
):
    ticket = await ticket_repository.get_by_id(ticket_id, db)

    if ticket is None:
        return None

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(ticket, key, value)

    return await ticket_repository.update(ticket, db)


async def delete_ticket(
    ticket_id: UUID,
    db: AsyncSession,
):
    ticket = await ticket_repository.get_by_id(ticket_id, db)

    if ticket is None:
        return False

    await ticket_repository.delete(ticket, db)
    return True