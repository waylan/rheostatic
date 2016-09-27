==========
Rheostatic
==========

.. default-role:: code

A Static File Server with options.

Installation
------------

To install Rheostatic run the following command::

    pip install https://github.com/waylan/rheostatic/archive/master.zip

Note that this is currently **alpha** software and not yet hosted on PyPI. As such, the
above command downloads the source code from GitHub. Upon a stable release, the package will
become available from PyPI.

Usage
-----

For usage, run `rheostatic --help`.

If the `rheostatic` command cannot be found, try running `python -m rheostatic` instead.

Dependencies
------------

Rheostatic is a pure Python library with no external dependencies. It should run without issue
on CPython versions 2.7, 3.3, 3.4, and 3.5 as well as `PyPy`_.

.. _`PyPy`: http://pypy.org/

License
-------

Rheostatic is licensed under the `MIT License`_ as defined in `LICENSE`.

.. _`MIT License`: https://opensource.org/licenses/MIT
