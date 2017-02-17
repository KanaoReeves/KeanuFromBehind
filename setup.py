from setuptools import setup, find_packages

setup(name="KeanuFromBehind",
      description="Backend end for keanu's frontend",
      author="",
      packages=find_packages(),
      install_requires=['flask', 'gunicorn', 'Flask-Autodoc'],
      )
