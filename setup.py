#!/usr/bin/env python
"""
Rheostatic - A Static File Server with options.

MIT License

Copyright (c) 2016 Waylan Limberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from setuptools import setup

with  open('README.rst', mode='r') as fd:
    long_description = fd.read()

from rheostatic import __version__

setup(
    name='Rheostatic',
    version=__version__,
    url='https://github.com/waylan/rheostatic',
    description='A Static File Server with options.',
    long_description=long_description,
    author='Waylan Limberg',
    author_email='waylan.limberg@icloud.com',
    license='MIT License',
    packages=['rheostatic', 'rheostatic.tests'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rheostatic = rheostatic.__main__:cli',
        ]
    },
    test_suite = 'rheostatic.tests',
    tests_require =['wsgi_intercept'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Utilities',
        'Intended Audience :: Developers'
    ]
)
