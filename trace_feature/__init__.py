# from .core.ruby.ruby_execution import RubyExecution

# def execute():
#     ex = RubyExecution()
#     ex.execute_scenario('/home/leticia/Documents/Desenho/trabalho2/myrottenpotatoes/features/adicionar_filme.feature', 10)

<<<<<<< cc8657541a6d2c1720904a09f49c77dbdd9bc888
=======
def execute():
    ex = RubyExecution()
    config = RubyConfig()
    if config.config():
        ex.execute_scenario('/home/bernardohrl/Documents/faculdade/8Semestre/Desenho/Projeto2/myrottenpotatoes/features/adicionar_filme.feature', 10)
    else:
        print('Error!!!')    
>>>>>>> Added feature information
