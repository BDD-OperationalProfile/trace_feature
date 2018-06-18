from trace_feature.core.base_config import BaseConfig
import os
import sys
import re

class RubyConfig(BaseConfig):
    def __init__(self):
        pass


    def config(self):
        if self.is_rails_project(self.get_local_path()):
            print('Rails project!')
        # Verificar requisitos
            if self.verify_requirements(self.get_local_path()):
                return True
            else:
                print('Set requirements')
                # INCLUIR REQUISITOS AQUI e rodar o bundle
        else:
            return False


    def is_rails_project(self, path):
        if os.path.exists(path + "/Gemfile"):
            return True
        else:
            return False


    # Adaptar de acordo com o que for feito com o @click
    def get_local_path(self):
        pathname = os.path.dirname(sys.argv[0])
        return os.path.abspath(pathname)


    def verify_requirements(self, path):
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
