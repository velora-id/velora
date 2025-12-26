from typing import List, Dict, Any
from .providers.base import LLMProvider
from src.credits.crud import get_credit_balance, deduct_credits
from src.core.firebase import get_db

class LLMClient:
    def __init__(self, providers: List[LLMProvider]):
        self.providers = providers

    def generate(self, prompt: str, organization_id: str, **kwargs) -> str:
        db = get_db()
        credit_balance = get_credit_balance(organization_id, db)
        
        # For now, we'll assume a fixed cost of 1 credit per request.
        # In a real-world scenario, this would be based on token usage.
        cost = 1 

        if credit_balance.balance < cost:
            raise Exception("Insufficient credits to generate a response.")

        for provider in self.providers:
            if provider.is_healthy():
                try:
                    response = provider.generate(prompt, **kwargs)
                    deduct_credits(organization_id, cost, db)
                    return response
                except Exception as e:
                    # Log the exception, but continue to the next provider
                    print(f"LLM provider failed: {e}")
                    continue
                    
        raise Exception("All LLM providers are unavailable.")
