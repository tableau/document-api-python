from setuptools import setup
    
setup(
    name='tableaudocumentapi',
    version='0.11',
    author='Tableau',
    author_email='github@tableau.com',
    url='https://github.com/tableau/document-api-python',
    packages=['tableaudocumentapi'],
    license='MIT',
    description='A Python module for working with Tableau files.',
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    test_suite='test',
    install_requires=['lxml']
)
