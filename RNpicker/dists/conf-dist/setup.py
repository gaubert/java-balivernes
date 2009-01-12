import os
from setuptools import setup, find_packages
version = '0.9'
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
      packages=['org','org.ctbto','org.ctbto.conf'],
      package_dir={'org.ctbto.conf': 'org/ctbto/conf'},
      package_data={'org.ctbto.conf': ['tests/test.config','tests/foo.config']},
      #data_files=[('/tmp/py-tests',['/home/aubert/dev/src-reps/java-balivernes/RNpicker/dists/conf-dist/tests/foo.config','/home/aubert/dev/src-reps/java-balivernes/RNpicker/dists/conf-dist/tests/test.config'])],
      install_requires=[]
      )
