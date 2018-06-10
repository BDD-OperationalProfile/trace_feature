import subprocess
import json
import sys, os
import re
from pprint import pprint

# subprocess.call(['cucumber', 'features/adicionar_filme.feature'])
#
# with open('coverage/cucumber/.resultset.json') as f:
#     data = json.load(f)
#
# pprint(data)

def verify_requirements(path):
    SIMPLECOV = "gem 'simplecov-json'"
    REQSIMCOV = "require 'simplecov-json'"
    START = "SimpleCov.start 'rails'"
    RESULT_DIR = "SimpleCov.coverage_dir 'coverage/cucumber'"


    with open(path+"/Gemfile", 'r') as file:

        if re.search(re.escape(SIMPLECOV), file.read(), flags=re.M) is None:
            return False

    file = open(path + "/features/support/env.rb", 'r')

    text_file = file.read()
    if re.search(re.escape(REQSIMCOV), text_file, flags=re.M) is None:
        print("Erro, inclua " + REQSIMCOV + " no arquivo /features/support/env.rb")
        return False
    if re.search(re.escape(START), text_file, flags=re.M) is None:
        print("Erro, inclua " + START + " no arquivo /features/support/env.rb")
        return False
    if re.search(re.escape(RESULT_DIR), text_file, flags=re.M) is None:
        print("Erro, inclua " + RESULT_DIR + " no arquivo /features/support/env.rb")
        return False

    return True

def include_requirements():
    pass

def execute_feature(path):
    feature_path = path + '/features/adicionar_filme.feature'
    print(feature_path)
    subprocess.call(['rails', 'cucumber', feature_path])
    print("AQUI FOI EM ")
    with open('coverage/cucumber/.resultset.json') as f:
        json_data = json.load(f)
        files = []
        lines = []
        for k in json_data:
            for i in json_data[k]['coverage']:
                # print(get_methods_from_feature(i, json_data[k]['coverage'][i]))
                if get_methods_from_feature(i, json_data[k]['coverage'][i]) is not None:
                    print("\ARQUIVO EXECUTADO: " + i)
                    # print("-------------------------------------\n")
                    print("LINHAS EXECUTADAS:\n")
                    for each in get_methods_from_feature(i, json_data[k]['coverage'][i]):
                        # print(each)
                        if "def" in each or "class" in each:
                            print(each)
                    print("-------------------------------------\n")
                # files.append(i)
                # lines.append(json_data[k]['coverage'][i])

                # print("\n\n\n\nasdjasiudhaisuhdauishdiuashdiuhasiudhas\n")
                # print(json_data[k]['coverage']['/Users/rafael/Documents/engSoftw/myrottenpotatoes/app/helpers/application_helper.rb'])
        #print(json_data.items())



def get_methods_from_feature(file, lines):
    result = []
    #print(lines)
    with open(file) as f:
        for line_number, line in enumerate(f, 1):
            # word = line.strip()
            if lines[line_number-1] is not None and lines[line_number-1] is not 0:
                # Verificar se a linha e um metodo ou classe, se for, verificar se alguma linha dentro desse metodo foi executada.
                # So nesse caso posso incluir esta linha como metodo ou classe executado.
                if len(line) > 0:
                    result.append(line)
    if result:
        return result
    else:
        return None
def create_result_json():
    pass

def is_rails_project(path):
    if os.path.exists(path + "/Gemfile"):
        return True
    else:
        return False


def get_local_path():
    pathname = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathname)

def execute():
    path = get_local_path()

    if is_rails_project(path) and verify_requirements(path):
        print('Este e um projeto rails!')
        execute_feature(path)
