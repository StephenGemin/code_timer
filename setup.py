from setuptools import setup

# read the contents of README file
from os import path
current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_desc = f.read()

setup(
  name='code_timer',
  packages=['code_timer'],
  version='1.1.7',
  license='MIT License',
  description='Custom timer for your Python coding pleasure',
  long_description=long_desc,
  long_description_content_type='text/markdown',
  author='Stephen Gemin',
  author_email='s.gemin88@gmail.com',
  url='https://github.com/StephenGemin/code_timer',
  download_url='https://github.com/StephenGemin/code_timer/',
  extras_require={
          'dev': [
              'pytest',
              'pytest-pep8',
              'pytest-cov'
          ]
  },
  keywords=["decorator", "decorators", "code timer", "timing",
            "code timing", "context manager", "profiling"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Debuggers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
