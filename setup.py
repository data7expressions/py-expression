#!/usr/bin/env python3
from setuptools import setup
# from distutils.core import setup
with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'py-expression',
  packages = ['py_expression'],
  version = '0.0.10',
  description = 'parser and solve expressions',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url = 'https://github.com/FlavioLionelRita/py-expression', # use the URL to the github repo
  download_url = 'https://github.com/FlavioLionelRita/py-expression/tarball/0.0.1',
  keywords = ['parser', 'expression'],
  classifiers = [],
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@hotmail.com'  
)