from trace_feature.core.base_execution import BaseExecution
from trace_feature.core.models import Feature, Method, ScenarioOutline, SimpleScenario
import linecache
import subprocess
import json


class RubyExecution(BaseExecution):
 
    def __init__(self):
        self.class_definition_line = None
        self.method_definition_lines = []

        self.feature = Feature()
        

    # this method will execute all the features at this project
    def execute(self):
        pass

    # this method will execute only a specific feature
    def execute_feature(self, feature_name):
        pass

    # this method will execute a specific scenario into a specific feature
    # filename: refer to the .feature file
    # scenario_ref: refer to the line or the name of a specific scenario
    def execute_scenario(self, feature_name, scenario_ref):
        # Vamos ter executar um cenario dentro do filename. O comando pra isso ta na issue. Executando isso,
        # o arquivo resultset.json sera criado. Ai vamos iterar sobre esse arquivo, a iteracao inicial nos da
        # o nome dos arquivos tocados. Ai com isso, basta usarmos os metodos do felipe e sair instanciando as modelos
        # com isso.. Depois que as modelos estiverem instanciadas, ja era, so gerar o json da modelo Feature, que
        # vai trazer todas as modelos relacionadas com ela no json, e fim.
        #primeiro executamos o cenario..
        subprocess.call(['rails', 'cucumber', feature_name])


        self.get_feature_information(feature_name) 
        

        with open('coverage/cucumber/.resultset.json') as f:
            json_data = json.load(f)
            for k in json_data:
                for i in json_data[k]['coverage']:
                    json_data[k]['coverage'][i]
                    self.run_file(i, json_data[k]['coverage'][i])



        print('\n\n\n\n')
        print(self.feature)
        print('\n\n\n\n')

        self.export_json()


    def run_file(self, filename, cov_result):
        self.method_definition_lines = []
        with open(filename) as file:
            if self.is_empty_class(file):
                return

            self.get_class_definition_line(file)
            self.get_method_definition_lines(file, cov_result)
            self.remove_not_executed_definitions(filename, cov_result)


            for method in self.method_definition_lines:
                new_method = Method()
                new_method.method_name = self.get_method_or_class_name(method, filename)
                new_method.class_name = self.get_method_or_class_name(self.class_definition_line, filename)
                new_method.class_path = filename
                self.feature.scenarios[0].executed_methods.append(new_method)

                

            


    def is_method(self, line):
        # We only want the first token in the line, to avoid false positives.
        # That is, the word 'def' appearing in some other context.
        tokens = line.split()
        if tokens:
            first_token = tokens[0]
            return first_token == 'def'
        return False

    def is_class(self, line):
        # We only want the first token in the line, to avoid false positives.
        # That is, the word 'class' appearing in some other context.
        tokens = line.split()
        if tokens:
            first_token = tokens[0]
            return first_token == 'class'
        return False

    def get_method_or_class_name(self, line_number, filename):
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
        file.seek(0)
        for line_number, line in enumerate(file, 1):
            if self.is_class(line):
                self.class_definition_line = line_number
                return

    def get_method_definition_lines(self, file, cov_result):
        file.seek(0)
        for line_number, line in enumerate(file, 1):
            if self.is_method(line):
                self.method_definition_lines.append(line_number)

    def remove_not_executed_definitions(self, filename, cov_result):
        # Methods that weren't executed aren't relevant, so we remove them here.
        for line in self.method_definition_lines:
            if not self.was_executed(line, filename, cov_result):
                self.method_definition_lines.remove(line)

    def was_executed(self, def_line, filename, cov_result):
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

        for line in range(def_line, end_line):
            if cov_result[line]:
                return True
        return False

    def is_empty_class(self, file):
        file.seek(0)
        for line in file:
            if self.is_method(line):
                return False
        return True





    def get_feature_information(self, path): 
        
        self.get_language(path)
        self.feature.path_name = path
        self.get_feature_name(path)

        self.get_scenarios(path)
        self.get_steps(path)


        
    
    def get_feature_name(self, path):
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "Funcionalidade: " in line:
                    self.feature.feature_name = line.split("Funcionalidade: ",1)[1] 
        return



    def get_scenarios(self, path):
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "Cenario: " in line:
                    # print ("Cenario: " + line.split("Delineacao do Cenario: ",1)[1])
                    new_scenario = SimpleScenario()
                    new_scenario.scenario_title = line.split("Cenario: ",1)[1]
                    new_scenario.line = line_number
                    self.feature.scenarios.append(new_scenario)
                    
        return


    def get_steps(self, path):
        qt_scenarios = len(self.feature.scenarios)
        key_words = ["Quando ", "E ", "Dado ", "Entao "]
        current_scenario = 0

        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if any(word in line for word in key_words):
                    self.feature.scenarios[current_scenario].steps.append(line)
                    
                    if "Entao " in line:
                        current_scenario+=1
                    
        return


    def get_language(self, path):
        with open(path) as file:
            file.seek(0)
            for line_number, line in enumerate(file, 1):
                if "#language:" in line:
                    self.feature.language = line.split("#language:",1)[1]

        return



    def export_json(self):        
        file = open('result.json', 'w')
        file.write(self.feature.toJSON())
