import click
import os

from trace_feature.core.base_execution import BaseExecution
from trace_feature.core.features.bdd_read import BddRead
from trace_feature.core.ruby.ruby_execution import RubyExecution
from trace_feature.core.ruby.ruby_config import RubyConfig


@click.command()
@click.option('--scenario', '-s', default=0, help='This is the scenario\'s correponding line that can be found at the feature file.')
@click.option('--feature', '-f', default='', help='This is the file\'s name where the feature is.')
@click.option('--project', '-p', default='.', help='This is the name of the project to be analyzed. Default: current folder.')
@click.option('--lista', '-l', is_flag=True, help='This option list all features into this project.')
def trace(lista, project, feature, scenario):
    """
        This command ables you to run the traces generator's tool by running every BDD feature.
        None of the arguments are required.
    """

    read = BddRead()
    if lista:
        read.list_all_features(os.path.abspath(project))

    if not lista:
        execution = None
        # language = find_language(path)
        language = 'Ruby'

        if language == 'Ruby':
            execution = RubyExecution()
            config = RubyConfig()
            if config.config() is False:
                print('Erro!')
                exit()
        if feature == '' and scenario == 0:
            project = os.path.abspath(project)
            execution.execute(project)

    # Where the function config_project has to be

    # if feature != '' and scenario == 0:
    #     print('feature')
    #     feature_name = os.path.join(click.get_app_dir(project), (feature + '.feature'))
    #     execution.feature(feature_name)
    # elif feature != '' and scenario != 0:
    #     print('scenario')
    #     feature_name = os.path.join(click.get_app_dir(project), (feature + '.feature'))
    #     execution.execute_scenario(feature_name, scenario)
    # elif feature == '' and scenario != 0:
    #     click.echo('Must define a feature to specify a scenario.')
