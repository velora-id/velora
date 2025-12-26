import requests
from typing import Dict, Any

def send_webhook(config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Sends a webhook to a specified URL with a given payload."""
    url = config.get('url')
    if not url:
        raise ValueError("Webhook URL is not defined in the action config.")

    payload = context.get('payload', {})

    response = requests.post(url, json=payload)

    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return {"status_code": response.status_code, "text": response.text}
