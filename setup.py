try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='tableaudocumentapi',
    version='0.1.0-dev',
    author='Tableau Software',
    author_email='github@tableau.com',
    url='https://github.com/tableau/document-api-python',
    py_modules=['tableaudocumentapi'],
    license='MIT',
    description='A Python module for working with Tableau files.',
    test_suite='test'
)
