from trace_feature.core.base_config import BaseConfig
import os
import sys
import re
import subprocess

class RubyConfig(BaseConfig):
    def __init__(self):
        pass

    def config(self):
        if self.is_rails_project(self.get_local_path()):
            print('Rails project!')
            if self.verify_requirements(self.get_local_path()):
                return True
            else:
                self.check_gemfile(self.get_local_path())
                subprocess.call(['bundle', 'install'], cwd=self.get_local_path())
                self.check_environment(self.get_local_path())
        else:
            return False


    def is_rails_project(self, path):
        if os.path.exists(path + "/Gemfile"):
            return True
        else:
            return False

    # Adaptar de acordo com o que for feito com o @click
    def get_local_path(self):
        # pathname = os.path.dirname(sys.argv[0])
        return '.'

    def verify_requirements(self, path):
        SIMPLECOV = '  gem \'simplecov-json\'\n'
        REQSIMCOV = 'require \'simplecov-json\''
        START = 'SimpleCov.start \'rails\''
        RESULT_DIR = 'SimpleCov.coverage_dir \'coverage/cucumber\''

        with open(path+"/Gemfile", 'r') as file:
            if re.search(re.escape(SIMPLECOV), file.read(), flags=re.M) is None:
                return False

        file = open(path + "/features/support/env.rb", 'r')
        text_file = file.read()
        if re.search(re.escape(REQSIMCOV), text_file, flags=re.M) is None:
            return False
        if re.search(re.escape(START), text_file, flags=re.M) is None:
            return False
        if re.search(re.escape(RESULT_DIR), text_file, flags=re.M) is None:
            return False
        return True

    def check_gemfile(self, path):
        SIMPLECOV = '  gem \'simplecov-json\'\n'
        output = []
        with open(path + '/Gemfile', 'r+') as file:
            has_simplecov = False
            is_on_test = False
            for line in file:
                tokens = line.split()
                if self.is_test_group(tokens):
                    is_on_test = True
                if is_on_test:
                    if not has_simplecov:
                        has_simplecov = self.simplecov_exists(tokens)
                    if tokens[0] == 'end':
                        if not has_simplecov:
                            simplecov_line = SIMPLECOV
                            output.append(simplecov_line)
                        is_on_test = False
                output.append(line)
            file.seek(0)
            file.writelines(output)

    def is_test_group(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == 'group' and tokens[1] == ':development,' and tokens[2] == ':test':
                return True
        return False

    def simplecov_exists(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == 'gem' and tokens[1] == '\'simplecov-json\'':
                return True
        return False

    def check_environment(self, path):
        REQSIMCOV = ' require \'simplecov-json\'\n'
        START = ' SimpleCov.start \'rails\'\n'
        RESULT_DIR = ' SimpleCov.coverage_dir \'coverage/cucumber\'\n'
        output = []
        with open(path + '/features/support/env.rb', 'r+') as file:
            has_req = False
            has_start = False
            has_result_dir = False

            for line in file:
                tokens = line.split()
                if self.req_simple_cov(tokens):
                    has_req = True
                if self.simple_cov_start(tokens):
                    has_start = True
                if self.result_dir(tokens):
                    has_result_dir = True
                output.append(line)
            if not has_req:
                has_req_line = REQSIMCOV
                output.insert(6, has_req_line)
            if not has_start:
                has_start_line = START
                output.insert(7, has_start_line)
            if not has_result_dir:
                has_result_line = RESULT_DIR
                output.insert(8, has_result_line)

            file.seek(0)
            file.writelines(output)

    def req_simple_cov(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == ' require' and tokens[1] == '\'simplecov-json\'':
                return True
        return False

    def simple_cov_start(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == ' SimpleCov.start' and tokens[1] == '\'rails\'':
                return True
        return False

    def result_dir(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == ' SimpleCov.coverage_dir and tokens[1] == \'coverage/cucumber\'':
                return True
        return False
