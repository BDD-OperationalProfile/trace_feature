from trace_feature.core.base_execution import BaseExecution
import linecache

class RubyExecution(BaseExecution):
    def __init__(self):
        self.definition_lines = []

    def execute(self):
        pass

    def is_method_or_class(self, line):
        # We only want the first token in the line, to avoid false positives.
        # That is, the words 'def' or 'class' appearing in some other context.
        tokens = line.split()
        if tokens:
            first_token = tokens[0]
            return first_token == 'def' or first_token == 'class'
        return False

    def get_method_or_class_name(self, line):            
        # The method or class name is always going to be the second token
        # in the line.
        name_token = line.split()[1]

        # If the method definition contains parameters, part of it will also
        # be in the token though. For example:
        #    def foo(x, y) 
        # would become 'foo(x,'. We then separate those parts.
        name, parenthesis, rest = name_token.partition('(')

        return name

    def get_definition_lines(self, filename):
        with open(filename) as file:
            for line_number, line in enumerate(file, 1):
                if self.is_method_or_class(line):
                    self.definition_lines.append({
                        line_number: self.get_method_or_class_name(line)
                    })
