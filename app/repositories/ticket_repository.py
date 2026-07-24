from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket


async def create(ticket: Ticket, db: AsyncSession):
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def get_all(db: AsyncSession):
    result = await db.execute(select(Ticket))
    return result.scalars().all()


async def get_by_id(ticket_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )
    return result.scalar_one_or_none()


async def update(ticket: Ticket, db: AsyncSession):
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def delete(ticket: Ticket, db: AsyncSession):
    await db.delete(ticket)
    await db.commit()