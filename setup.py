"""Darwinex APIs setup script."""

import sys
from pathlib import Path

from setuptools import setup, find_packages

here = Path(__file__).parent.resolve()

__version__ = None
with open(here / 'version.py') as f:
    exec(f.read())
print(here)

with open(here / 'README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='darwinexapis',
    version=__version__,
    description='Python wrapper for Darwinex APIs',
    long_description=long_description,
    url='https://github.com/darwinex/darwinexapis',
    author='Alpha Team @ DWX',
    author_email='content@darwinex.com',
    license='BSD',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    platforms = ['any'],
    keywords='darwinex algorithmic trading quant quantitative analysis asyncio websockets darwins async',
    #package_dir={"": "darwinexapis"},
    include_package_data=True,
    packages=find_packages(),
    #package_data={'darwinexapis':['*']},
    install_requires=['pandas',
                      'plotly', 
                      'matplotlib', 
                      'requests', 
                      'websockets',
                      'tqdm',
                      'dash',
                      'pyftpdlib',
                      'tables',
                      'matplotlib'
                      ]
)
