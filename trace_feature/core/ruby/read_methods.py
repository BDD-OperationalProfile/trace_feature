import json
import os

import requests

from trace_feature.core.models import Method
from trace_feature.core.ruby.ruby_execution import RubyExecution


def read_methods(path):
    methods = []
    ruby_exec = RubyExecution()
    exclude = ['migrations', 'db', '.git', 'log', 'public', 'script', 'spec', 'tmp',
               'vendor', 'lib', 'docker', 'db', 'coverage', 'config', 'bin', 'features']
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith(".rb"):
                file_path = os.path.join(root, file)
                with open(file_path) as fp:
                    if ruby_exec.is_empty_class(fp):
                        pass
                    else:
                        ruby_exec.get_class_definition_line(fp)
                        methods_line = get_methods_line(fp, ruby_exec)
                        for method in methods_line:
                            # print('method: ', method)
                            if method is not None:
                                new_method = Method()
                                new_method.method_name = ruby_exec.get_method_or_class_name(method, file_path)
                                if ruby_exec.class_definition_line is None:
                                    new_method.class_name = 'None'
                                else:
                                    new_method.class_name = ruby_exec.get_method_or_class_name(
                                        ruby_exec.class_definition_line, file_path)
                                new_method.class_path = file_path
                                new_method.method_id = file_path + ruby_exec.get_method_or_class_name(method, file_path)
                                methods.append(new_method)
    return methods


def get_methods_line(fp, ruby):
    fp.seek(0)
    methods = []
    for line_number, line in enumerate(fp, 1):
        if ruby.is_method(line):
            methods.append(line_number)
    return methods


def send_all_methods(methods):
    json_string = json.dumps([ob.__dict__ for ob in methods])
    # file.write(json_string)
    r = requests.post("http://localhost:8000/createmethods", json=json_string)
    print(r.status_code, r.reason)
