from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.schemas.ticket import CreateTicketRequest, UpdateTicketRequest


async def create_ticket(
    data: CreateTicketRequest,
    db: AsyncSession,
):
    ticket = Ticket(
        title=data.title,
        priority=data.priority,
        status="open",
    )

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    return ticket


async def get_all(db: AsyncSession):
    result = await db.execute(select(Ticket))
    return result.scalars().all()


async def get_ticket(
    ticket_id: UUID,
    db: AsyncSession,
):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    return result.scalar_one_or_none()


async def update_ticket(
    ticket_id: UUID,
    data: UpdateTicketRequest,
    db: AsyncSession,
):
    ticket = await get_ticket(ticket_id, db)

    if ticket is None:
        return None

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(ticket, key, value)

    await db.commit()
    await db.refresh(ticket)

    return ticket


async def delete_ticket(
    ticket_id: UUID,
    db: AsyncSession,
):
    ticket = await get_ticket(ticket_id, db)

    if ticket is None:
        return False

    await db.delete(ticket)
    await db.commit()

    return True