from string import Template
from typing import Dict, Any

def render_prompt(template_string: str, context: Dict[str, Any]) -> str:
    """Renders a prompt template with the given context."""
    template = Template(template_string)
    return template.safe_substitute(context)
