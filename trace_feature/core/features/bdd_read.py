import json
import os

from trace_feature.core.models import Feature, SimpleScenario


class BddRead:
    def __init__(self):
        self.features = []
        self.num_files = 0
        self.num_func = 0

    def list_all_features(self, initial_path):
        """
        This method show all BDD features into a specific project, with the scenarios and steps.
        :param initial_path: The base path of this project.
        :return: print all features.
        """

        print('------------------------')
        print('Numero de arquivos analisados: ', self.num_files)
        print('Numero de features analisadas:', len(self.features))
        print('------------------------')
        with open('result.json', 'w+') as file:
            json_string = json.dumps(self.features, default=Feature.obj_dict)
            file.write(json_string)

    def get_all_features(self, url):
        """
        This method get all features, scenarios and steps
        :param url: base path of the project.
        :return: a list of Features
        """
        self.load_infos(url)
        return self.features

    def load_infos(self,  url):
        """
        This method will instantiate all features with their scenarios
        :param url: base path of the project.
        :return: all features with their scenarios.
        """
        for root, dirs, files in os.walk(url):
            for file in files:
                if file.endswith(".feature"):
                    self.num_files += 1
                    feature = self.get_feature_information(os.path.join(root, file))
                    self.features.append(feature)

    def get_feature_information(self, path):
        """Get all information in a .feature file.
        :param path: the path of the .feature file.
        :return: feature information instantiated.
        """
        feature = Feature()
        feature.language = self.get_language(path)
        feature.path_name = path
        feature.feature_name = self.get_feature_name(path)
        feature.scenarios = self.get_scenarios(path)
        # feature = self.get_steps(path, feature)
        return feature

    def get_feature_name(self, path):
        """This method get the feature name.
        :param path: the path to this feature file.
        :return: the name of the feature.
        """
        feature_name = ''
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "Funcionalidade: " in line:
                    feature_name = line.split("Funcionalidade: ", 1)[1].replace('\n', '')
        return feature_name

    def get_steps(self, lines, initial, final):
        """
        This method get all steps into a specific scenario.
        :param lines: Content of the file.
        :param initial: The line of the beginning of this scenario
        :param final: The last line of this scenario.
        :return: a list of Steps.
        """
        key_words = ["Quando ", "E ", "Dado ", "Entao "]
        steps = []
        index = initial
        if final is not None:
            while index <= final:
                if any(word in lines[index-1] for word in key_words):
                    steps.append(lines[index-1].replace('\n', '').replace('  ', ''))
                index += 1
        else:
            while index <= len(lines):
                if any(word in lines[index-1] for word in key_words):
                    steps.append(lines[index-1].replace('\n', '').replace('  ', ''))
                index += 1
        return steps

    def read_scenario(self, path, initial_line, final_line):
        """
        This method read a specific scenario.
        :param path: Path of the file containing the scenario.
        :param initial_line: The line of the beginning of this scenario
        :param final_line: Last line of this scenario.
        :return: A scenario instantiated.
        """
        scenario = SimpleScenario()
        with open(path) as file:
            file.seek(0)
            lines = file.readlines()
            scenario.scenario_title = lines[initial_line-1].split("Cenario: ", 1)[1].replace('\n', '').replace(':', '')
            scenario.line = initial_line
            scenario.steps = self.get_steps(lines, initial_line+1, final_line)
        return scenario

    def get_scenarios(self, path):
        """This method get all scenarios of a feature.
        :param path: the path to the feature file.
        :return: all scenarios instantiated.
        """
        scenarios = []
        lines_scenarios = self.get_all_scenarios_lines(path)
        count = len(lines_scenarios)

        for index in range(count):
            scenario = SimpleScenario()
            if index + 1 >= count:
                scenario = self.read_scenario(path, lines_scenarios[index], None)
            else:
                scenario = self.read_scenario(path, lines_scenarios[index], lines_scenarios[index+1]-1)

            scenarios.append(scenario)
        return scenarios

    def get_language(self, path):
        """Get the language of the .feature file.
        :param path: the path to the .feature file.
        :return: language.
        """
        language = ''
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "#language:" in line:
                    language = line.split("#language:", 1)[1].replace('\n', '')
        return language

    def get_all_scenarios_lines(self, path):
        """
        This method get the lines of each scenario into a specific file.
        :param path: The path of this file.
        :return: The lines.
        """
        lines = []
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "Cenario:" in line:
                    lines.append(line_number)
        return lines
