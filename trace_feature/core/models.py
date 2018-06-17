from abc import ABC, abstractmethod

class Feature:

    def __init__(self):
        self.path_name = ""
        self.feature_name = ""
        self.scenarios = []
        self.language = ""
        self.user_story = "" 
        self.background = None





class Method:

    def __init__(self):
        self.method_name = ""
        self.class_name = ""
        self.class_path = ""


    def __str__(self):
        return "\t" + self.method_name + " (" + self.class_name + "):  " + self.class_path  




class Scenario(ABC):

    def __init__(self):
        steps = NotImplemented
        scenario_title = NotImplemented
        line = NotImplemented


    # @property
    # def steps(self):
    #     raise NotImplementedError
    
    # @property
    # def scenario_title(self):
    #     raise NotImplementedError

    # @property
    # def line(self):
    #     raise NotImplementedError

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def set_line(self):
        pass




class SimpleScenario(Scenario):

    def __init__(self):
        self.steps = []
        self.scenario_title = ""
        self.line = None
        self.executed_methods = []

    def execute(self):
        pass

    def set_line(self):
        pass


    def __str__(self):
        print("\n Title: " + self.scenario_title)
        self.print_methods()
        return "\n"

    def print_methods(self):
        for method in self.executed_methods:
            print(method)





class ScenarioOutline(Scenario):

    def __init__(self):
        self.steps = []
        self.scenario_title = ""
        self.line = None
        self.examples = []
        self.scenario_iterations = []

    def execute(self):
        pass

    def set_line(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def execute(self):
        pass


