"""
Package configuration file
"""
from setuptools import find_packages, setup

setup(
    name='IXDjango',
    version='0.1.4',
    author='Infoxchange Australia dev team',
    author_email='devs@infoxchange.net.au',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/IXDjango/',
    license='MIT',
    description='Management commands for deploying Django projects.',
    long_description=open('README').read(),
    install_requires=[
        "Django >= 1.3.0",
    ],
    tests_require=[
        "pep8 >= 1.4.6",
        "pylint >= 0.28.0",
        "pylint-mccabe >= 0.1.3",
    ],
)
