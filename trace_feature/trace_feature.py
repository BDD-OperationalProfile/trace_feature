import json
import signal

import click
import os

from trace_feature.core.features.gherkin_parser import read_all_bdds
from trace_feature.core.ruby.read_methods import read_methods, send_all_methods, install_excellent_gem, analyse_methods
from trace_feature.core.ruby.ruby_execution import RubyExecution
from trace_feature.core.ruby.ruby_config import RubyConfig


@click.command()
@click.option('--scenario', '-s', default=0, help='This is the scenario\'s correponding line that can be found at the feature file.')
@click.option('--feature', '-f', default='', help='This is the file\'s name where the feature is.')
@click.option('--project', '-p', default='.', help='This is the name of the project to be analyzed. Default: current folder.')
@click.option('--lista', '-l', is_flag=True, help='This option list all features into this project.')
@click.option('--spec', '-t', is_flag=True, help='This option execute spec files tests into this project.')
@click.option('--methods', '-m', is_flag=True, help='This option read all methods into this project.')
@click.option('--analyse', '-a', is_flag=True, help='This option analyse all methods into this project.')
@click.option('--without', '-w', is_flag=True, help='This option run features without analysis.')
def trace(without, analyse, methods, spec, lista, project, feature, scenario):
    """
        This command ables you to run the traces generator's tool by running every BDD feature.
        None of the arguments are required.
    """

    if lista:
        features = read_all_bdds(os.path.abspath(project))
        for feature in features:
            print(feature)

        num_scenarios = 0
        num_steps = 0

        with open('features.txt', 'w') as file:
            print('Projeto:', 'SISBOL', file=file)
            for feature in features:
                print('\tFeature:', feature.feature_name, file=file)
                num_scenarios += len(feature.scenarios)
                print('\tNúmero de Cenários: ', len(feature.scenarios), file=file)
                print('\tPath: ', feature.path_name, file=file)
                print('\tLinguagem: ', feature.language, file=file)
                print('\tCenarios: ', file=file)
                for scenario in feature.scenarios:
                    print('\t\tCenario: ', scenario.scenario_title, file=file)
                    print('\t\tNúmero de Steps: ', len(scenario.steps), file=file)
                    print('\t\tSteps:', file=file)
                    num_steps += len(scenario.steps)
                    for step in scenario.steps:
                        print('\t\t\tKeyword: ', step.keyword, file=file)
                        print('\t\t\tTexto: ', step.text, file=file)

            print('\n\n\n-------------------------------------------------------------------------------------------', file=file)
            print('Number of Features: ', len(features), file=file)
            print('Number of Scenarios: ', num_scenarios, file=file)
            print('Number of Steps: ', num_steps, file=file)

    else:
        if without:
            print('Sem perda de tempo')
            execution = RubyExecution()
            execution.execute_without_inst()

        elif methods:
            project_methods = read_methods(os.path.abspath(project))
            install_excellent_gem()
            project_methods.methods = analyse_methods(project_methods.methods)
            send_all_methods(project_methods)
            for method in project_methods.methods:
                print('Name: ', method.method_name)
                print('Path: ', method.class_path)
            print(len(project_methods.methods))
        elif analyse:
            project_methods = read_methods(os.path.abspath(project))
            install_excellent_gem()
            project_methods.methods = analyse_methods(project_methods.methods)
        else:
            #  TODO language = find_language(path)
            language = 'Ruby'

            if language == 'Ruby':
                execution = RubyExecution()
                config = RubyConfig()
                if config.config() is False:
                    print('Error!')
                    exit()
                elif spec:
                    # project_methods = read_methods(os.path.abspath(project))
                    # install_excellent_gem()
                    # project_methods.methods = analyse_methods(project_methods.methods)
                    # send_all_methods(project_methods)
                    execution.execute_specs(os.path.abspath(project))
                else:
                    # print('Read methods..')
                    # project_methods = read_methods(os.path.abspath(project))
                    # install_excellent_gem()
                    # project_methods.methods = analyse_methods(project_methods.methods)
                    # send_all_methods(project_methods)
                    if feature and scenario:
                        print('feature and scenario')
                        execution.prepare_scenario(feature, int(scenario))
                    elif feature != '':
                        print('feature')
                        project = os.path.abspath(project)
                        execution.execute_feature(project, feature)
                    else:
                        print('Full Execution!')
                        project = os.path.abspath(project)
                        execution.execute(project)

