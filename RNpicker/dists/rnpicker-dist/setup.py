import os
from setuptools import setup, find_packages
version = '0.8.0'
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
      #packages=find_packages(),
      packages=['ctbto','ctbto.common','ctbto.db','ctbto.query','ctbto.renderers','ctbto.tests','ctbto.transformer'],
      package_dir={'ctbto.tests': 'ctbto/tests'},
      package_dir={'ctbto.tests': 'ctbto/tests'},
      package_data={'ctbto.tests': ['conf_tests/rnpicker.config','conf_tests/pretty-print.xslt','conf_tests/scripts/*.sh','conf_tests/samples/*.master','conf_tests/templates/*.html']},
      install_requires=['conf>=0.8.0','SQLAlchemy>=0.4.7','cx-Oracle>=4.3','lxml>=2.0']
      )
