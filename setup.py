from distutils.core import setup
import os

curr_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(curr_dir, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='code_timer',
  packages=['code_timer'],
  version='v1.0.0',
  license='MIT',
  description='Custom timer for your Python coding pleasure',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Stephen Gemin',
  author_email='s.gemin88@gmail.com',
  url='https://github.com/StephenGemin/code_timer',
  download_url='https://github.com/StephenGemin/code_timer/archive/v1.0.0.tar.gz',
  keywords=["decorator", "decorators", "code timer", "timing",
            "code timing", "context manager", "profiling"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
