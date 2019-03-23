#!/usr/bin/env python

from distutils.core import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(name='Pando',
      version='1.0',
      description='Diagnostic Decision Tree Generator',
      author='Kier von Konigslow',
      author_email='kvonkonigslow@gmail.com',
      url='kvonkonigslow.com/Pando',
      packages=['pando'],
      install_requires=install_requires
     )
