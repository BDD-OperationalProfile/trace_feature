from abc import ABC, abstractmethod

class BaseExecution(ABC):
    @abstractmethod
    def execute(self):
        pass