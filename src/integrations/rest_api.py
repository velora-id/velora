import requests
from typing import Dict, Any
from .base import Integration

class RestApiConnector(Integration):
    def execute(self, config: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Makes a request to a REST API."""
        method = data.get('method', 'GET').upper()
        headers = data.get('headers', {})
        params = data.get('params')
        json_data = data.get('json')

        response = requests.request(
            method=method,
            url=config.get('base_url') + data.get('path', ''),
            headers=headers,
            params=params,
            json=json_data
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status_code": response.status_code, "text": response.text}
