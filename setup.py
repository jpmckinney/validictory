from setuptools import find_packages, setup

from validictory import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(name='validictory',
      version=__version__,
      description='general purpose python data validator',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='James Turk',
      author_email='james.p.turk@gmail.com',
      url='http://github.com/jamesturk/validictory',
      license='MIT',
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   'Programming Language :: Python :: 3.11',
                   'Programming Language :: Python :: 3.12',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Programming Language :: Python :: Implementation :: PyPy',
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      packages=find_packages(exclude=['validictory.tests', 'validictory.tests.*']),
      extras_require={
          'test': [
              'pytest',
              'pytest-cov',
          ]
      }
)
