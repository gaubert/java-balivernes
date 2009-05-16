import os
#from setuptools import setup, find_packages
from distutils.core import setup


version = '1.2.2'
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
      scripts=['scripts/generate_arr','scripts/generate_products_and_email'],
      packages=['ctbto','ctbto.common','ctbto.db','ctbto.email','ctbto.query','ctbto.renderers','ctbto.run','ctbto.tests','ctbto.transformer'],
      package_dir={'ctbto.tests': 'ctbto/tests'},
      package_data={'ctbto.tests': ['conf_tests/rnpicker.config','conf_tests/pretty-print.xslt','conf_tests/scripts/*.sh','conf_tests/samples/*.master','conf_tests/templates/*.html']},
      # copy extra files from first val in tuple to second. Everything is always done from --root that is sys.prefix by default
      data_files=[('conf',['conf/rnpicker.config','conf/pretty-print.xslt']),('conf/scripts',['conf/scripts/remote_extraction_from_archive.sh']),('conf/templates',['conf/templates/ArrHtml.html'])],
      #install_requires=['conf>=0.8.0','SQLAlchemy>=0.4.7','cx-Oracle>=4.3','lxml>=2.0']
      )
