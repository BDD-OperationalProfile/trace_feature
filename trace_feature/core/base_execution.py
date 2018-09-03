from abc import ABC, abstractmethod


class BaseExecution(ABC):
    @abstractmethod
    def execute(self, path):
        pass

    # this method will execute only a specific feature
    @abstractmethod
    def execute_feature(self, filename):
        pass

    # this method will execute a specific scenario into a specific feature
    # filename: refer to the .feature file
    # scenario_ref: refer to the line or the name of a specific scenario
    @abstractmethod
    def execute_scenario(self, filename, scenario_ref):
        pass
