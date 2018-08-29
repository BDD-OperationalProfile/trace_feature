import os

import nltk as nltk

from trace_feature.core.models import Feature, Scenario, SimpleScenario


class BddRead:
    def __init__(self):
        self.features = []
        self.num_files = 0
        self.num_func = 0

    def list_all_features(self, initial_path):
        print('------------------------')
        self.load_infos(initial_path)
        print('Numero de arquivos analisados: ', self.num_files)
        # print('Numero de funcionalidades: ', num_func)

    def load_infos(self,  url):
        for root, dirs, files in os.walk(url):
            for file in files:
                if file.endswith(".feature"):
                    self.num_files += 1
                    feature = self.get_feature_information(os.path.join(root, file))
                    self.features.append(feature)
                    print('---------------------------------------------')
                    print(feature)
                    print('---------------------------------------------')

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
        self.get_steps(path, feature)

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

    def get_scenarios(self, path):
        """This method get all scenarios of a feature.
        :param path: the path to the feature file.
        :return: all scenarios instantiated.
        """
        scenarios = []
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "Cenario: " in line:
                    # print ("Cenario: " + line.split("Delineacao do Cenario: ",1)[1])
                    new_scenario = SimpleScenario()
                    new_scenario.scenario_title = line.split("Cenario: ", 1)[1].replace('\n', '')
                    new_scenario.line = line_number
                    scenarios.append(new_scenario)
        return scenarios

    def get_steps(self, path, feature):
        """This method get all steps into each scenario of a feature.
        :param path: the path to the feature file.
        :return: all steps instantiated.
        """
        print('arquivo: ', feature.path_name)
        print('tamanho: ', len(feature.scenarios))
        key_words = ["Quando ", "E ", "Dado ", "Entao "]
        current_scenario = 0
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if any(word in line for word in key_words):
                    feature.scenarios[current_scenario].steps.append(line.replace('\n', ''))

                    if feature.scenarios[current_scenario+1].line-1 == line_number:
                        current_scenario += 1
                    # if "Entao " in line:
                    #     current_scenario += 1
        return

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
                    language = line.split("#language:",1)[1].replace('\n', '')
        return language
