from distutils.core import setup
#
# find_packages comes in handy for deep trees. see
# http://bruno.im/2010/may/05/packaging-django-reusable-app/
#
from setuptools import find_packages

setup(
    name='IXDjango',
    version='0.1.0',
    author='IXA dev team',
    author_email='development@infoxchange.net.au',
    packages=find_packages(),
    url='',
    license='',
    description='Bunch of tools useful to all IX Django projects.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.3.0",
        "pep8 >= 1.0.1",
        "pylint >= 0.25.1"
    ],
)


