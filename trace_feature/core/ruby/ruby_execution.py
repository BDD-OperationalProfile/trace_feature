from trace_feature.core.base_execution import BaseExecution
import linecache

class RubyExecution(BaseExecution):
    def __init__(self):
        self.class_definition_line = None
        self.method_definition_lines = []

    def execute(self):
        pass

    def run_file(self, filename, cov_result):
        with open(filename) as file:
            if self.is_empty_class(file):
                return
            
            self.get_class_definition_line(file)
            self.get_method_definition_lines(file, cov_result)

            print('Executed class: ', self.get_method_or_class_name(self.class_definition_line, filename))
            print('Executed methods:')
            for method in self.method_definition_lines:
                print(self.get_method_or_class_name(method, filename))

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

        # Methods that weren't executed aren't relevant, so we remove them here.
        for line in self.method_definition_lines:
            if not self.was_executed(line, cov_result):
                self.method_definition_lines.remove(line)     
   
    def was_executed(self, def_line, cov_result):
        # We consider that the lines containing a method go from its definition
        # until the definition of the next method. Blank lines are getting 
        # considered this way, but they don't really interfere.
        position = self.method_definition_lines.index(def_line)
        try:
            end_def = self.method_definition_lines[position + 1]
        # If it's the last method definition, we consider its end as the end of
        # the file.
        except IndexError:
            end_def = len(cov_result)

        for line in range(def_line, end_def - 1):
            if cov_result[line]:
                return True
        return False

    def is_empty_class(self, file):
        file.seek(0)
        for line in file:
            if self.is_method(line):
                return False
        return True