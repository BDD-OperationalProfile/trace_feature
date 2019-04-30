import os

import requests
from trace_feature.core.ruby.spec_models import It

from trace_feature.core.base_execution import BaseExecution
from trace_feature.core.features.gherkin_parser import read_all_bdds, get_scenario, read_feature
from trace_feature.core.models import Feature, Method, SimpleScenario, Project
import linecache
import subprocess
import json
import re

from trace_feature.core.ruby.ruby_spec_execution import read_specs


class RubyExecution(BaseExecution):

    def __init__(self):
        self.class_definition_line = None
        self.method_definition_lines = []
        self.project = Project()
        self.feature = Feature()
        self.scenario = SimpleScenario()
        self.it = It()

    def execute_specs(self, path):
        specs = read_specs(path)
        self.project = self.get_project_infos(path)
        for spec in specs:
            self.method_definition_lines = []
            self.class_definition_line = []
            self.it = spec
            self.it.project = self.project
            self.execute_it(self.it)

    def prepare_scenario(self, feature_path, scenario_line):
        scenario = get_scenario(feature_path, scenario_line)
        self.execute_scenario(feature_path, scenario)

    def execute_it(self, it):
        print('Executing It: ', it.description)
        # signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        p = subprocess.Popen(["bundle", "exec", "rspec", it.file + ":" + str(it.line)],
                             stdout=subprocess.PIPE)

        # Catches Tuple first element and decode it                     
        test_message = p.communicate()[0]
        test_message = test_message.decode('utf-8')
        

        # Parses test_message to get number of examples, peding e failures
        # using regex lib re

        test_examples = re.findall(r"[0-9]+ examples", test_message) 
        test_pended = re.findall(r"[0-9]+ pending", test_message) 
        test_failed = re.findall(r"[0-9]+ failures", test_message) 


        # Then print all together
        if test_pended:
            print("\n" + test_pended[0] + " tests \n") 
        else:
            print("There are no pending tests. \n")

        if test_failed:
            print(test_failed[0] + " tests in this it block \n") 
        else:
            print("There are no failed tests. \n")


        # And make a comparison to see if there are no failed nor
        # pended tests
        if not (len(test_failed) and len(test_pended)):
            test_success = test_examples[0].split('examples')[0]
            print(test_success + "tests successed \n")

        # try:
        #     p.stdout.close()
        # except BrokenPipeError:
        #     pass
        # p.wait()
        # TODO: analyse this print
        with open('coverage/cucumber/.resultset.json') as f:
            json_data = json.load(f)
            for k in json_data:
                for i in json_data[k]['coverage']:
                    if i:
                        self.run_file_with_it(i, json_data[k]['coverage'][i], it)
        self.it.project = self.project
        self.it.key = it.file + str(it.line)
        print('Number of executed Methods: ', str(len(it.executed_methods)))
        print(self.it.description)
        print('Linha: ', self.it.line)
        print('Arquivo: ', self.it.file)
        print('Métodos: ', self.it.executed_methods)

        dado = input('Type Enter to continue..')
        self.send_information(False)

    # this method will execute all the features at this project
    def execute(self, path):
        # Cleaning data
        # self.class_definition_line = None
        # self.method_definition_lines = []
        # self.project = Project()
        # self.feature = Feature()
        # self.scenario = SimpleScenario()

        self.project = self.get_project_infos(path)

        # Getting all features from this project
        features = read_all_bdds(path)

        for feature in features:
            self.method_definition_lines = []
            self.class_definition_line = None
            feature.project = self.project
            self.feature = feature

            print('Execute Feature: ', feature.feature_name)
            for scenario in feature.scenarios:
                self.execute_scenario(feature.path_name, scenario)

            self.send_information(True)

    # this method will execute only a specific feature
    def execute_feature(self, project, feature_name):
        """This method will execute only a specific feature
        :param feature_name: define the feature that will be executed
        :return: a json file with the trace.
        """
        self.project = self.get_project_infos(project)
        feature = read_feature(feature_name)
        self.method_definition_lines = []
        self.class_definition_line = None
        feature.project = self.project
        self.feature = feature
        print('Execute Feature: ', feature.feature_name)
        for scenario in feature.scenarios:
            self.execute_scenario(feature.path_name, scenario)
        self.send_information(True)
    # this method will execute a specific scenario into a specific feature
    # filename: refer to the .feature file
    # scenario_ref: refer to the line or the name of a specific scenario
    def execute_scenario(self, feature_name, scenario):
        """This Method will execute only a specific scenario
        :param feature_name: define the feature that contains this scenario
        :param scenario: contains a key to get a scenario
        :return: a json file with the trace.
        """
        # print(subprocess.check_output("RAILS_ENV=development"))
        # os.environ['RAILS_ENV'] = "test"
        print('Executing Scenario: ', scenario.scenario_title)
        # signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        p = subprocess.Popen(["bundle", "-v"], stdout=subprocess.PIPE)
        print(p.communicate())
        p = subprocess.Popen(["bundle", "exec", "rake", "cucumber", "FEATURE=" + feature_name + ":" + str(scenario.line)],
                         stdout=subprocess.PIPE)
        print(p.communicate())
        # try:
        #     p.stdout.close()
        # except BrokenPipeError:
        #     pass
        # p.wait()
        # TODO: analyse this print
        with open('coverage/cucumber/.resultset.json') as f:
            json_data = json.load(f)
            for k in json_data:
                for i in json_data[k]['coverage']:
                    if i:
                        self.run_file(i, json_data[k]['coverage'][i], scenario)
        print('Number of executed Methods: ', str(len(scenario.executed_methods)))

    def run_file_with_it(self, filename, cov_result, it):
        """This method will execute a specific feature file
        :param filename: the  name of the feature file
        :param cov_result: a array containing the result os simpleCov for some method
        :param scenario: contains the line where the scenario starts
        :return: Instantiate the Methods executed.
        """
        self.method_definition_lines = []
        with open(filename) as file:
            if self.is_empty_class(file):
                return

            self.get_class_definition_line(file)
            self.get_method_definition_lines(file, filename, cov_result)
            for method in self.method_definition_lines:
                if method is not None:
                    new_method = Method()
                    new_method.method_name = self.get_method_or_class_name(method, filename)
                    if self.class_definition_line is None:
                        new_method.class_name = 'None'
                    else:
                        new_method.class_name = self.get_method_or_class_name(self.class_definition_line, filename)
                    new_method.class_path = filename
                    new_method.method_id = filename + self.get_method_or_class_name(method, filename)
                    it.executed_methods.append(new_method)

    def run_file(self, filename, cov_result, scenario):
        """This method will execute a specific feature file
        :param filename: the  name of the feature file
        :param cov_result: a array containing the result os simpleCov for some method
        :param scenario: contains the line where the scenario starts
        :return: Instantiate the Methods executed.
        """
        self.method_definition_lines = []
        with open(filename) as file:
            if self.is_empty_class(file):
                return

            self.get_class_definition_line(file)
            self.get_method_definition_lines(file, filename, cov_result)
            for method in self.method_definition_lines:
                if method is not None:
                    new_method = Method()
                    new_method.method_name = self.get_method_or_class_name(method, filename)
                    if self.class_definition_line is None:
                        new_method.class_name = 'None'
                    else:
                        new_method.class_name = self.get_method_or_class_name(self.class_definition_line, filename)
                    new_method.class_path = filename
                    new_method.method_id = filename + self.get_method_or_class_name(method, filename)
                    scenario.executed_methods.append(new_method)

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
            return first_token == 'class' or first_token == 'module'
        return False

    def get_method_or_class_name(self, line_number, filename):
        """Method that get the name of Methods and Classes
        :param line_number: the number of the line.
        :param filename: the file that contains this line.
        :return: String Name.
        """
        line = linecache.getline(filename, line_number)

        name = 'None'
        # The method or class name is always going to be the second token
        # in the line.
        if len(line.split()) > 1:
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
        return

    def get_method_definition_lines(self, file, filename, cov_result):
        """This method get the line where a method is defined.
        :param file: The file that contains this method.
        :param cov_result: contains the result of simplecov.
        :param filename: contains the name of the analysed file.
        :return: the number of the line.
        """
        file.seek(0)
        for line_number, line in enumerate(file, 1):
            # print('dentro')
            if self.is_method(line):
                if self.was_executed(line_number, filename, cov_result):
                    print('Get Method: ', line)
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

        block_tokens = ['do', 'case', 'for', 'begin', 'while']

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

        for line in range(def_line, end_line):
            if cov_result[line]:
                return True
        return False

    def is_empty_class(self, file):
        """Verify if a class contains any method
        :param file: file that will be analysed.
        :return: True if is empty, and False if not.
        """
        file.seek(0)
        for line in file:
            if self.is_method(line):
                return False
        return True

    def send_information(self, bdd):
        """This method will export all data to a json file.
        :return: json file.
        """
        if bdd:
            json_string = json.dumps(self.feature, default=Feature.obj_dict)
            # file.write(json_string)
            r = requests.post("http://localhost:8000/createproject", json=json_string)
            print(r.status_code, r.reason)
        else:
            json_string = json.dumps(self.it, default=It.obj_dict)
            # file.write(json_string)
            r = requests.post("http://localhost:8000/covrel/update_spectrum", json=json_string)
            print(r.status_code, r.reason)

    def get_project_infos(self, path):
        project = Project()
        project.language = "Ruby on Rails"
        project.repository = self.verify_git_repository(path)
        project.name = self.get_name_project(path)

        return project

    def verify_git_repository(self, path):
        git_path = path + "/.git/"
        if os.path.exists(git_path):
            with open(git_path + 'config') as file:
                for line in file:
                    if 'url =' in line:
                        url = line.split(' = ')
                        return url[1]
        return None

    def get_name_project(self, path):
        path = path.split('/')
        return path[-1]
