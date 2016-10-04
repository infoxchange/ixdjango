"""
Package configuration file
"""
from setuptools import find_packages, setup

setup(
    name='IXDjango',
    version='1.0.2',
    author='Infoxchange Australia dev team',
    author_email='devs@infoxchange.net.au',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/IXDjango/',
    license='MIT',
    description='Management commands for deploying Django projects.',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.7.0",
        "httplib2",
        "future",
        "six",
    ],
    tests_require=[
        "pep8 >= 1.6.2",
        "pylint >= 1.4.1",
        "pylint-mccabe >= 0.1.3",
    ],
)
