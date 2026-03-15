import logging
from dataclasses import KW_ONLY, dataclass, field

import requests

from .base import AIError

logger = logging.getLogger(__package__)


DEFAULT_API_ENDPOINT = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_API_VERSION = "2023-06-01"


class AnthropicError(AIError):
    pass


@dataclass
class ChatAnthropic:
    token: str
    _: KW_ONLY
    system_prompt: str | None = None
    timeout: float = 15.0
    temperature: float = 0.7
    max_tokens: int = 1000
    model: str | None = None
    api_endpoint: str = None
    session: requests.Session = field(default_factory=requests.Session)

    def __post_init__(self) -> None:
        self.api_endpoint = self.api_endpoint or DEFAULT_API_ENDPOINT
        self.model = self.model or DEFAULT_MODEL

    def _default_headers(self) -> dict[str, str]:
        return {
            "x-api-key": self.token,
            "anthropic-version": DEFAULT_API_VERSION,
            "content-type": "application/json",
        }

    def send_message(self, message: str) -> str:
        payload: dict = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": message}],
        }

        # Системный промпт передается отдельным полем, не в messages
        if self.system_prompt:
            payload["system"] = self.system_prompt

        try:
            response = self.session.post(
                self.api_endpoint,
                json=payload,
                headers=self._default_headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            if "error" in data:
                raise AnthropicError(data["error"]["message"])

            assistant_message = data["content"][0]["text"]

            return assistant_message

        except requests.exceptions.RequestException as ex:
            raise AnthropicError(f"Network error: {ex}") from ex
