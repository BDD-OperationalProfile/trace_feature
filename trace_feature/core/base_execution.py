from abc import ABCMeta, abstractmethod

class BaseExecution(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def execute(self):
        pass