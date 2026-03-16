from abc import ABC, abstractmethod

class BaseAI(ABC):
    @abstractmethod
    def generate_response(self, prompt:str) -> str:
        pass