# price_providers.py
from abc import ABC, abstractmethod

class PriceProvider(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def fetch_price(self, card_name: str) -> float:
        pass
