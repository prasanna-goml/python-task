from typing import Literal

from pydantic import BaseModel, field_validator


class CreateTicketRequest(BaseModel):
    title: str
    priority: Literal["low", "medium", "high"]

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank.")

        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters.")

        return value
from typing import Optional, Literal

class UpdateTicketRequest(BaseModel):
    title: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["open", "in_progress", "resolved"]] = None
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank.")

        return value
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict, computed_field


class TicketResponse(BaseModel):
    id: UUID
    title: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved"]
    created_at: datetime

