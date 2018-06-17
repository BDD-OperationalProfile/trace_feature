from .core.ruby.ruby_execution import RubyExecution
from .core.ruby.ruby_config import RubyConfig


def execute():
    ex = RubyExecution()
    config = RubyConfig()
    if config.config():
        ex.execute_scenario('/home/leticia/Documents/Desenho/trabalho2/myrottenpotatoes/features/adicionar_filme.feature', 10)
    else:
        print('Error!!!')    
