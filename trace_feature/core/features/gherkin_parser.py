import os
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner
from trace_feature.core.models import Feature, SimpleScenario, StepBdd


def get_scenario(feature_path, line):
    with open(feature_path) as fp:
        fp.seek(0)
        parser = Parser()
        print(feature_path)
        feature_file = parser.parse(TokenScanner(fp.read()))
        scenarios = get_scenarios(feature_file['feature']['children'])
        for each in scenarios:
            if each.line == line:
                return each
        return None


def read_all_bdds(url):
    features = []
    for root, dirs, files in os.walk(url + '/features/'):
        for file in files:
            if file.endswith(".feature"):
                feature = Feature()
                file_path = os.path.join(root, file)
                with open(file_path) as fp:
                    fp.seek(0)
                    parser = Parser()
                    print(file_path)
                    feature_file = parser.parse(TokenScanner(fp.read()))

                    feature.feature_name = feature_file['feature']['name']
                    feature.language = feature_file['feature']['language']
                    feature.path_name = file_path
                    feature.tags = feature_file['feature']['tags']
                    feature.line = feature_file['feature']['location']['line']
                    feature.scenarios = get_scenarios(feature_file['feature']['children'])

                    features.append(feature)
    return features


def read_feature(feature_path):
    """
    Read a specific feature
    :param feature_path: path of the file that contains the feature
    :return: Feature object
    TODO: Refactor to use this method into for loop in read_all_bdds() method
    """
    feature = Feature()
    with open(feature_path) as fp:
        fp.seek(0)
        parser = Parser()
        print(feature_path)
        feature_file = parser.parse(TokenScanner(fp.read()))

        feature.feature_name = feature_file['feature']['name']
        feature.language = feature_file['feature']['language']
        feature.path_name = feature_path
        feature.tags = feature_file['feature']['tags']
        feature.line = feature_file['feature']['location']['line']
        feature.scenarios = get_scenarios(feature_file['feature']['children'])

    return feature


def get_scenarios(childrens):
    scenarios = []
    for children in childrens:
        scenario = SimpleScenario()
        scenario.line = children['location']['line']
        scenario.scenario_title = children['name']
        scenario.steps = get_steps(children['steps'])

        scenarios.append(scenario)
    return scenarios


def get_steps(steps):
    all_steps = []
    for each_step in steps:
        step = StepBdd()
        step.line = each_step['location']['line']
        step.keyword = each_step['keyword']
        step.text = each_step['text']

        all_steps.append(step)

    return all_steps