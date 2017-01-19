from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as file:
    long_description = file.read()

setup(
    name='nessus',
    version='0.0',
    description='Tenable Nessus API SDK',
    long_description=long_description,
    author='Code Particle',
    packages=find_packages(exclude=['doc', 'tests*']),
    install_requires=[
        "mock==2.0.0",
        "pytest ==3.0.4",
        "requests==2.12.1",
        "six==1.10.0",
        "Sphinx==1.5.1",
    ],
)
