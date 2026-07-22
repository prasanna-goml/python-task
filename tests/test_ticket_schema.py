import pytest
from pydantic import ValidationError

from app.schemas.ticket import CreateTicketRequest


def test_blank_title():
    with pytest.raises(ValidationError):
        CreateTicketRequest(
            title="   ",
            priority="high"
        )


def test_short_title():
    with pytest.raises(ValidationError):
        CreateTicketRequest(
            title="ab",
            priority="high"
        )


def test_valid_title():
    ticket = CreateTicketRequest(
        title="Printer Issue",
        priority="high"
    )

    assert ticket.title == "Printer Issue"