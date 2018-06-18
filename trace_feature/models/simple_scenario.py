from trace_feature.models.scenario import Scenario

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
        return ""

    def print_methods(self):
        for method in self.executed_methods:
            print(method)
