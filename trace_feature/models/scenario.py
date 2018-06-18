from abc import ABC, abstractmethod


class Scenario(ABC):

    @property
    def steps(self):
        raise NotImplementedError
    
    @property
    def scenario_title(self):
        raise NotImplementedError

    @property
    def line(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def set_line(self):
        pass
