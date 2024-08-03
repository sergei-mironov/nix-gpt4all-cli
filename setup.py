import sys
from os import environ, system
from os.path import join, dirname
from setuptools import setup, find_packages
from logging import getLogger
from subprocess import check_output
logger=getLogger(__name__)
warning=logger.warning

VERSION:str|None
try:
  with open('semver.txt') as f:
    VERSION = str(f.read()).strip()
except Exception:
  VERSION = None

REVISION:str|None
try:
  REVISION=environ["GPT4ALLCLI_REVISION"]
except Exception as e:
  warning("Couldn't read GPT4ALLCLI_REVISION, trying `git rev-parse`")
  cmd = ['git', 'rev-parse', 'HEAD']
  cwd = None
  try:
    cwd = dirname(__file__) or '.'
    REVISION=check_output(cmd, cwd=cwd).decode().strip()
  except Exception as e:
    warning(e)
    warning(f"Couldn't use `{cmd}` in `{cwd}`, no revision metadata will be set")
    REVISION=None

with open(join('python','sm_aicli', 'revision.py'), 'w') as f:
  f.write("# AUTOGENERATED by setup.exe!\n")
  if VERSION:
    f.write(f"VERSION = '{VERSION}'\n")
  else:
    f.write(f"VERSION = None # Undefined at the time of packaging'\n")
  if REVISION:
    f.write(f"REVISION = '{REVISION}'\n")
  else:
    f.write(f"REVISION = None # Undefined at the time of packaging\n")

gpt4all = 'gpt4all-bindings' if 'NIX_PATH' in environ else 'gpt4all >= 2.7.0'

with open("README.md", "r") as f:
  long_description = f.read()

setup(
  name="sm-aicli",
  zip_safe=False, # https://mypy.readthedocs.io/en/latest/installed_packages.html
  version=VERSION,
  package_dir={'':'python'},
  packages=find_packages(where='python'),
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=[gpt4all, 'openai', 'gnureadline', 'lark'],
  scripts=[join('.','python','aicli')],
  python_requires='>=3.6',
  author="Sergei Mironov",
  author_email="sergei.v.mironov@proton.me",
  url='https://github.com/sergei-mironov/aicli',
  description="Command-line interface for a number of AI models",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX :: Linux",
    "Topic :: Software Development :: Build Tools",
    "Intended Audience :: Developers",
    "Development Status :: 3 - Alpha",
  ],
)
