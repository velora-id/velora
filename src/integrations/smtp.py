import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any
from .base import Integration

class SmtpEmailSender(Integration):
    def execute(self, config: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Sends an email using SMTP."""
        msg = MIMEText(data.get('body'))
        msg['Subject'] = data.get('subject')
        msg['From'] = config.get('from_address')
        msg['To'] = data.get('to_address')

        with smtplib.SMTP(config.get('host'), config.get('port')) as server:
            server.starttls()
            server.login(config.get('username'), config.get('password'))
            server.send_message(msg)

        return {"status": "success"}
