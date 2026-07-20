from typing import Optional

from fastapi import APIRouter, HTTPException

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
def create_ticket(ticket: CreateTicketRequest):
    return ticket_service.create_ticket(ticket)

@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
):
    return ticket_service.get_all(status, priority)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str):
    ticket = ticket_service.get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: str, data: UpdateTicketRequest):
    ticket = ticket_service.update_ticket(ticket_id, data)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: str):
    deleted = ticket_service.delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deleted successfully"}