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
            self.verify_requirements(self.get_local_path()):
            subprocess.call(['bundle', 'install'], cwd=self.path)
        else:
            return False


    def is_rails_project(self, path):
        for root, _, files in os.walk(path):
            for filename in files:
                if filename == 'Gemfile':
                    try:
                        open(os.path.join(path, filename))
                    except IOError:
                        return False
                    else:
                        self.gemfile = os.path.join(path, filename)
                        return True

    # Adaptar de acordo com o que for feito com o @click
    def get_local_path(self):
        pathname = os.path.dirname(sys.argv[0])
        return os.path.abspath(pathname)


    def verify_requirements(self, path):
        self.check_gemfile(path)
        self.check_environment(path)

    def check_gemfile(self, path):
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
                            simplecov_line = '  gem \'simplecov\', :require => false\n'
                            output.append(simplecov_line)
                        is_on_test = False
                output.append(line)
            file.seek(0)
            file.writelines(output)

    def is_test_group(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == 'group' and tokens[1] == ':test':
                return True
        return False

    def simplecov_exists(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == 'gem' and tokens[1] == '\'simplecov\',':
                return True
        return False

    def check_environment(self, path):
        output = []
        with open(path + '/env.rb', 'r+') as file:
            has_gem = False
            for line in file:
                tokens = line.split()
                if self.is_gem_instantiated(tokens):
                    has_gem = True
                output.append(line)
            if not has_gem:
                simplecov_line = ' SimpleCov.start \'rails\'\n'
                output.insert(1, simplecov_line)
            file.seek(0)
            file.writelines(output)
    
    def is_gem_instantiated(self, tokens):
        if len(tokens) > 1:
            if tokens[0] == 'SimpleCov.start' and tokens[1] == '\'rails\'':
                return True
        return False