from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Ticket:
    id: UUID
    title: str
    priority: str
    status: str
    created_at: datetime