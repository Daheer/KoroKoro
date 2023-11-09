from setuptools import setup, find_packages

def get_requirements():
  with open('requirements.txt') as f:
    requirements = f.read().splitlines()
  if '-e .' in requirements:
    requirements.remove('-e .')
  return requirements

setup(
  name='KoroKoro',
  version='1.0.0',
  description='Dahiru Ibrahim',
  author='suhayrid6@gmail.com',
  author_email='suhayrid6@gmail.com',
  packages=find_packages(),
  install_requires=get_requirements(),
)