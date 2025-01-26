import requests

from core.interfaces.observer_interface import Observer


class DiscordNotifier(Observer):
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url: str = webhook_url

    def update(self, message: str) -> None:
        payload: dict[str, str] = {"content": f"- `{message}`"}
        requests.post(self.webhook_url, json=payload)
