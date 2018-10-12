import os
from time import sleep

from trace_feature.core.features.bdd_read import BddRead

from trace_feature.core.base_execution import BaseExecution
from trace_feature.core.features.gherkin_parser import read_all_bdds
from trace_feature.core.models import Feature, Method
import linecache
import subprocess
import json
import requests


class RubyExecution(BaseExecution):

    def __init__(self):
        self.class_definition_line = None
        self.method_definition_lines = []

        self.feature = Feature()

    # this method will execute all the features at this project
    def execute(self, path):
        read = BddRead()
        features = read_all_bdds(path)

        for feature in features:
            print('----------------------------------------------------------')
            print(feature)
            print('----------------------------------------------------------')
        exit()
        # features = read.get_all_features(path)
        for feature in features:
            self.method_definition_lines = []
            self.class_definition_line = None
            self.feature = feature
            print('ANALISANDO FEATURE: ', feature.feature_name)
            self.execute_scenario(feature.path_name, 10)

    # this method will execute only a specific feature
    def execute_feature(self, feature_name):
        """This method will execute only a specific feature
        :param feature_name: define the feature that will be executed
        :return: a json file with the trace.
        """
        pass

    # this method will execute a specific scenario into a specific feature
    # filename: refer to the .feature file
    # scenario_ref: refer to the line or the name of a specific scenario
    def execute_scenario(self, feature_name, scenario_ref):
        """This Method will execute only a specific scenario
        :param feature_name: define the feature that contains this scenario
        :param scenario_ref: contains a key to get a scenario
        :return: a json file with the trace.
        """

        subprocess.call(['rails', 'cucumber', feature_name])
        # self.get_feature_information(feature_name)
        sleep(5)

        with open('coverage/cucumber/.resultset.json') as f:
            json_data = json.load(f)
            for k in json_data:
                for i in json_data[k]['coverage']:
                    self.run_file(i, json_data[k]['coverage'][i])

        self.export_json()

    def run_file(self, filename, cov_result):
        """This method will execute a specific feature file
        :param filename: the  name of the feature file
        :param cov_result: a array containing the result os simpleCov for some method
        :return: Instantiate the Methods executed.
        """
        self.method_definition_lines = []
        with open(filename) as file:
            if self.is_empty_class(file):
                return

            self.get_class_definition_line(file)
            self.get_method_definition_lines(file, filename, cov_result)
            # self.remove_not_executed_definitions(filename, cov_result)

            for method in self.method_definition_lines:
                new_method = Method()
                new_method.method_name = self.get_method_or_class_name(method, filename)
                new_method.class_name = self.get_method_or_class_name(self.class_definition_line, filename)
                new_method.class_path = filename
                new_method.method_id = filename + self.get_method_or_class_name(method, filename)
                self.feature.scenarios[0].executed_methods.append(new_method)

    def is_method(self, line):
        """Verify if is the line is a method definition.
        :param line: Line content.
        :return: True if is a method definition, False if not.
        """
        # We only want the first token in the line, to avoid false positives.
        # That is, the word 'def' appearing in some other context.
        tokens = line.split()
        if tokens:
            first_token = tokens[0]
            return first_token == 'def'
        return False

    def is_class(self, line):
        """Verify if this line is a class definition.
        :param line: Line content.
        :return: true if is a class, false if not.
        """
        # We only want the first token in the line, to avoid false positives.
        # That is, the word 'class' appearing in some other context.
        tokens = line.split()
        if tokens:
            first_token = tokens[0]
            return first_token == 'class'
        return False

    def get_method_or_class_name(self, line_number, filename):
        """Method that get the name of Methods and Classes
        :param line_number: the number of the line.
        :param filename: the file that contains this line.
        :return: String Name.
        """
        line = linecache.getline(filename, line_number)

        # The method or class name is always going to be the second token
        # in the line.
        name_token = line.split()[1]

        # If the method definition contains parameters, part of it will also
        # be in the token though. For example:
        #    def foo(x, y)
        # would become 'foo(x,'. We then separate those parts.
        name, parenthesis, rest = name_token.partition('(')

        return name

    def get_class_definition_line(self, file):
        """This method get the line where a class is defined.
        :param file: the file that contains this class.
        :return: the number of the line.
        """
        file.seek(0)
        for line_number, line in enumerate(file, 1):
            if self.is_class(line):
                self.class_definition_line = line_number
                return

    def get_method_definition_lines(self, file, filename, cov_result):
        """This method get the line where a method is defined.
        :param file: The file that contains this method.
        :param cov_result: .
        :return: the number of the line.
        """
        file.seek(0)
        for line_number, line in enumerate(file, 1):
            if self.is_method(line):
                if self.was_executed(line_number, filename, cov_result):
                    self.method_definition_lines.append(line_number)

    def remove_not_executed_definitions(self, filename, cov_result):
        """Remove all definitions that was not executed.
        :param filename: the file that contains this definitions.
        :param cov_result: json containing the simpleCov result.
        :return: definitions removed.
        """
        # Methods that weren't executed aren't relevant, so we remove them here.
        for line in self.method_definition_lines:
            if not self.was_executed(line, filename, cov_result):
                self.method_definition_lines.remove(line)

    def was_executed(self, def_line, filename, cov_result):
        """Verify if a definitions was executed.
        :param def_line: Line of a definition.
        :param filename: the file that contains this definition.
        :param cov_result: simpleCov json result.
        :return: True if was executed, and False if not.
        """
        # We go through the file from the line containing the method definition
        # until its matching 'end' line. We need to keep track of the 'end'
        # keyword appearing in other contexts, e.g. closing other blocks of code.
        remaining_blocks = 1
        current_line = def_line

        block_tokens = ['do', 'if', 'case', 'for', 'begin', 'while']

        while remaining_blocks:
            line = linecache.getline(filename, current_line)
            tokens = line.split()
            # If we have a line that requires a matching 'end', we increase the
            # number of blocks.
            if any(token in tokens for token in block_tokens):
                remaining_blocks += 1
            # Likewise, if we found an 'end', we decrease the number of blocks.
            # When it gets to zero, that means we have reached the end of the
            # method.
            if 'end' in tokens:
                remaining_blocks -= 1
            current_line += 1

        end_line = current_line - 1

        # Possivel erro dos métodos não tocados pode estar aqui!!!!!!! OLHA AQUI !!!!!!!!!!!!!
        i = 0
        print('----------VERIFICANDO METODO:')
        for line in range(def_line, end_line):
            if cov_result[line]:
                print("FOI TOCADO CARALHO: ", cov_result[line], "- Array ", line+5, " - Linha: ", line+1)
                return True
        return False

    def is_empty_class(self, file):
        """Verify if a class is empty
        :param file: file that will be analysed.
        :return: True if is empty, and False if not.
        """
        file.seek(0)
        for line in file:
            if self.is_method(line):
                return False
        return True

    def export_json(self):
        """This method will export all data to a json file.
        :return: json file.
        """

        with open(self.feature.feature_name + '_result.json', 'w+') as file:
            json_string = json.dumps(self.feature, default=Feature.obj_dict)
            file.write(json_string)
            # r = requests.post("http://localhost:8000/createproject", json=json_string)
            # print(r.status_code, r.reason)
