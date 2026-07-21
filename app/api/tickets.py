from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.schemas.ticket import (
    CreateTicketRequest,
    UpdateTicketRequest,
    TicketResponse,
)
from app.services import ticket_service

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket: CreateTicketRequest,
    db: AsyncSession = Depends(get_db),
):
    return await ticket_service.create_ticket(ticket, db)


@router.get("/", response_model=list[TicketResponse])
async def get_tickets(
    db: AsyncSession = Depends(get_db),
):
    return await ticket_service.get_all(db)


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    ticket = await ticket_service.get_ticket(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: UUID,
    data: UpdateTicketRequest,
    db: AsyncSession = Depends(get_db),
):
    ticket = await ticket_service.update_ticket(ticket_id, data, db)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    deleted = await ticket_service.delete_ticket(ticket_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deleted successfully"}