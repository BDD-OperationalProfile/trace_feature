from abc import ABC, abstractmethod

class BaseConfig(ABC):
    @abstractmethod
    def config(self):
        pass
