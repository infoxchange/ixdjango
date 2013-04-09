"""
Package configuration file
"""
from distutils.core import setup
from setuptools import find_packages

setup(
    name='IXDjango',
    version='0.1.2',
    author='Infoxchanhe Australia dev team',
    author_email='devs@infoxchange.net.au',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/IXDjango/',
    license='MIT',
    description='Management commands for deploying Django projects.',
    long_description=open('README').read(),
    install_requires=[
        "Django >= 1.3.0",
        "flake8 >= 2.0",
        "pylint >= 0.27.0"
    ],
)
