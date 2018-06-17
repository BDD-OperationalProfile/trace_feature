from setuptools import setup

setup(name='trace_feature',
      version='0.1',
      description='A lib to trace bdd features.',
      url='https://github.com/BDD-OperationalProfile/trace_feature',
      author='Rafael Fazzolino',
      author_email='fazzolino29@gmail.com',
      license='MIT',
      packages=['trace_feature', 'trace_feature.core', 'trace_feature.core.ruby'],
      zip_safe=False)
