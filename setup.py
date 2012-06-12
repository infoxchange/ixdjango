"""
Package configuration file
"""
from distutils.core import setup
from setuptools import find_packages

setup(
    name='IXDjango',
    version='0.1.0',
    author='Infoxchanhe Australia dev team',
    author_email='devs@infoxchange.net.au',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/IXDjango/',
    license='MIT',
    description='Management commands for deploying Django projects.',
    long_description=open('README').read(),
    install_requires=[
        "Django >= 1.3.0",
        "pep8 >= 1.0.1",
        "pylint >= 0.25.1"
    ],
)
