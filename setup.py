from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tableaudocumentapi',
    version='0.12',
    author='Justin Bisal',
    author_email='justin@viz-explainer.com',
    url='https://github.com/jbisal/document-api-python',
    packages=['tableaudocumentapi'],
    license='MIT',
    description='A Python module for working with Tableau files, with version-control diff engine and MCP integration.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    test_suite='test',
    install_requires=['lxml', 'pandas', 'fastmcp'],
    entry_points={
        'console_scripts': [
            'twb-diff=tableaudocumentapi.cli:main',
        ],
    }
)