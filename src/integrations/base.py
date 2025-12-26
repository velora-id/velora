from abc import ABC, abstractmethod
from typing import Dict, Any

class Integration(ABC):
    @abstractmethod
    def execute(self, config: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        pass
