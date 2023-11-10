from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str='requirements.txt') -> List[str]:
  with open(file_path) as f:
    requirements = f.read().splitlines()
  if '-e .' in requirements:
    requirements.remove('-e .')
  return requirements

setup(
  name='KoroKoro',
  version='1.0.0',
  description='See your e-commerce products in 3D',
  author='Dahiru Ibrahim',
  author_email='suhayrid6@gmail.com',
  packages=find_packages(),
  install_requires=get_requirements(),
)