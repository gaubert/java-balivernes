import os
from setuptools import setup, find_packages
version = '0.1.0'
README = os.path.join(os.path.dirname(__file__), 'README.txt')
long_description = open(README).read() + 'nn'
setup(name='RNPicker',
      version=version,
      description=("Software for exporting the RN Data as XML, "
                    "from CTBTO (www.ctbto.org)"),
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        ("Topic :: RadioNuclide Processing :: Libraries :: Python Modules"),
        ],
      keywords='radionuclide xml ',
      author='Guillaume Aubert',
      author_email='guillaume.aubert@ctbto.org',
      url='http://www.ctbto.org',
      license='Apache 2.0',
      packages=find_packages(),
      namespace_packages=['ctbto'],
      install_requires=['SQLAchemy']
      )
