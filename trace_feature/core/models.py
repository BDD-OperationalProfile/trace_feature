from abc import ABC, abstractmethod


class Project:
    def __init__(self):
        self.name = ""
        self.language = ""
        self.repository = ""
        self.methods = []

    def __str__(self):
        print('PROJETO:')
        print("\t name: " + self.name)
        print("\t language: " + self.language)
        print("\t Repository: " + str(self.repository))

        return ''

    def obj_dict(self):
        return self.__dict__


class Feature:

    def __init__(self):
        self.path_name = ""
        self.feature_name = ""
        self.scenarios = []
        self.language = ""
        self.user_story = ""
        self.tags = []
        self.line = None
        self.background = None
        self.project = ""

    def __str__(self):
        return self.feature_name

    def obj_dict(self):
        return self.__dict__


class Scenario(ABC):

    def __init__(self):
        steps = NotImplemented
        scenario_title = NotImplemented
        line = NotImplemented
        executed_methods = NotImplemented


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

    def obj_dict(self):
        return self.__dict__

    def execute(self):
        pass

    def set_line(self):
        pass

    def __str__(self):
        print("SCENARIO:")
        print("\t title: " + self.scenario_title)
        print("\t line: " + str(self.line))
        print("\t steps: ")

        for step in self.steps:
            print("\t\t" + step.keyword + step.text)

        for method in self.executed_methods:
            print('\t\t', method)

        return ''


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


class StepBdd:
    def __init__(self):
        self.line = None
        self.keyword = ""
        self.text = ""

    def obj_dict(self):
        return self.__dict__


class Method:

    def __init__(self):
        self.line = None
        self.method_id = ""
        self.method_name = ""
        self.class_name = ""
        self.class_path = ""
        self.abc_score = 0
        self.complexity = 0
        self.number_of_lines = 0
        self.content = ""

    def __str__(self):
        print("METHOD:")
        print("\t\t\t name: " + self.method_name)
        print("\t\t\t classe: " + self.class_name)
        print("\t\t\t path: " + self.class_path)
        return ''

    def obj_dict(self):
        return self.__dict__
