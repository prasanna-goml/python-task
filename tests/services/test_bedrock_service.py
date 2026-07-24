import json
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from app.services.aws.bedrock_service import (
    BedrockService,
    BedrockServiceError,
    FakeBedrockService,
)




def test_summarize_ticket_returns_summary_and_response():
    client = Mock()

    response = {
        "output": {
            "message": {
                "content": [
                    {
                        "text": json.dumps(
                            {
                                "summary": "Printer not working",
                                "suggested_response": "Restart the printer.",
                            }
                        )
                    }
                ]
            }
        }
    }

    client.converse.return_value = response

    service = BedrockService(client=client)
    service.model_id = "fake-model"

    result = service.summarize_ticket("Printer is offline.")

    assert result["summary"] == "Printer not working"
    assert result["suggested_response"] == "Restart the printer."

    client.converse.assert_called_once()


def test_fake_bedrock_service_returns_deterministic_response():
    service = FakeBedrockService()

    result = service.summarize_ticket("Cannot login to the application")

    assert "Support issue" in result["summary"]
    assert "investigated" in result["suggested_response"]



def test_handles_markdown_json_response():
    client = Mock()

    markdown_json = """```json
{
    "summary":"Email issue",
    "suggested_response":"Check SMTP server."
}
```"""

    client.converse.return_value = {
        "output": {
            "message": {
                "content": [
                    {
                        "text": markdown_json
                    }
                ]
            }
        }
    }

    service = BedrockService(client=client)
    service.model_id = "fake-model"

    result = service.summarize_ticket("Emails are failing.")

    assert result["summary"] == "Email issue"
    assert result["suggested_response"] == "Check SMTP server."


def test_fake_service_truncates_long_description():
    service = FakeBedrockService()

    description = "A" * 200

    result = service.summarize_ticket(description)

    assert result["summary"].startswith("Support issue:")
    assert len(result["summary"]) < 100




def test_raises_error_when_bedrock_request_fails():
    client = Mock()

    client.converse.side_effect = ClientError(
        {
            "Error": {
                "Code": "ValidationException",
                "Message": "Invalid request",
            }
        },
        "Converse",
    )

    service = BedrockService(client=client)
    service.model_id = "fake-model"

    with pytest.raises(BedrockServiceError, match="Bedrock request failed"):
        service.summarize_ticket("Test ticket")


def test_raises_error_when_invalid_json_returned():
    client = Mock()

    client.converse.return_value = {
        "output": {
            "message": {
                "content": [
                    {
                        "text": "This is not JSON"
                    }
                ]
            }
        }
    }

    service = BedrockService(client=client)
    service.model_id = "fake-model"

    with pytest.raises(
        BedrockServiceError,
        match="Bedrock returned an invalid response",
    ):
        service.summarize_ticket("Test ticket")