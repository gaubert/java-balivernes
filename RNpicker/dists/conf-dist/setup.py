import os
from setuptools import setup, find_packages
version = '0.8'
README = os.path.join(os.path.dirname(__file__), 'README.txt')
long_description = open(README).read() + 'nn'
setup(name='conf',
      version=version,
      description=("Conf a class for powerfully accessing configuration files, "
                    "from CTBTO (www.ctbto.org)"),
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        ("Topic :: Util :: Libraries :: Python Modules"),
        ],
      keywords='configuration, resources',
      author='Guillaume Aubert',
      author_email='guillaume.aubert@ctbto.org',
      url='http://www.ctbto.org',
      license='Apache 2.0',
      packages=find_packages(),
      namespace_packages=['org'],
      install_requires=[]
      )
