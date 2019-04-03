#!/usr/bin/env python

from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(name='Osler',
      version='0.1',
      description='Diagnostic Decision Tree Generator',
      author='Kier von Konigslow',
      author_email='kvonkonigslow@gmail.com',
      url='kvonkonigslow.com/Osler',
      packages=['osler'],
      install_requires=install_requires
     )
