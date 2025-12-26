import requests
from typing import Dict, Any
from .base import Integration

class WebhookSender(Integration):
    def execute(self, config: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Sends a webhook to a specified URL."""
        response = requests.post(config.get('url'), json=data)
        response.raise_for_status()
        return response.json()
