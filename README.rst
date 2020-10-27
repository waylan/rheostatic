==========
Rheostatic
==========

.. default-role:: code

A Static File Server with options.

Features
========

* A dedicated static file server.
* Emulates common behaviors of various popular servers (index files,
  extensionless files, index directories, etc.) See `options`_ for specifics.
* Serves custom error pages.
* Does not require the server root to be the current working directory.
* |build| |coverage| |status| |version| |format| |pyversions| |license|

.. |build| image:: https://github.com/waylan/rheostatic/workflows/CI/badge.svg?event=push
   :target: https://github.com/waylan/rheostatic/actions?query=workflow%3ACI+event%3Apush
.. |coverage| image:: https://codecov.io/gh/waylan/rheostatic/branch/master/graph/badge.svg?token=1v2THBaa3X
   :target: https://codecov.io/gh/waylan/Rheostatic
.. |status| image:: https://img.shields.io/pypi/status/rheostatic.svg
   :target: https://pypi.org/project/Rheostatic/
.. |version| image:: https://img.shields.io/pypi/v/rheostatic.svg
   :target: https://pypi.org/project/Rheostatic/
.. |format| image:: https://img.shields.io/pypi/format/rheostatic.svg
   :target: https://pypi.org/project/Rheostatic/#files
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/rheostatic.svg
   :target: https://pypi.org/project/Rheostatic/
.. |license| image:: https://img.shields.io/pypi/l/rheostatic.svg
   :target: https://opensource.org/licenses/MIT

.. contents:: Table of Contents
   :backlinks: top

Installation
============

To install Rheostatic run the following command::

    pip install rheostatic

Dependencies
------------

Rheostatic is a pure Python library with no external dependencies. It should run
without issue on CPython versions 3.6, 3.7, 3.8, and 3.9 as well as `PyPy3`_.

.. _PyPy3: http://pypy.org/

Use as a Command Line Tool
==========================

From the root directory of your site, run the command ``rheostatic``::

    $ cd /var/www
    $ rheostatic
    Starting server at http://localhost:8000/...
    Serving files from /var/www
    Press ctrl+c to stop.

Alternatively, pass the root directory to the ``rheostatic`` command::

    $ rheostatic path/to/root
    Starting server at http://localhost:8000/...
    Serving files from /absolute/path/to/root
    Press ctrl+c to stop.

For detailed usage instructions and options, run ``rheostatic --help``.

If the ``rheostatic`` command cannot be found, try running
``python -m rheostatic`` instead.

Use as a Python Library
=======================

For basic usage, import the ``rheostatic.serve`` function, which accepts any and
all `options`_ as keywords::

    from rheostatic import serve

    serve(address=('0.0.0.0', 80), root='/some/path', default_type='text/plain')

Note that ``address`` expects a tuple of the ``host`` and ``port``. The ``host``
must be a string and the ``port`` an integer. All other keywords correspond to
the available `options`_.

Under the hood, the ``serve`` function creates an instance of the class
``rheostatic.base.Rheostatic`` and passes it to a simple wsgi server as a wsgi
application. For lower level usage, an instance of the class may be created and
passed to any wsgi server. When initializing the class, you may pass in any
`options`_ as keywords::

    from rheostatic.base import Rheostatic

    app = Rheostatic(root='/some/path', index_file='README.html')

``Rheostatic`` accepts keywords which correspond to any of the available
`options`_. All options are also stored as attributes on the class instance::

    print app.root

Preparing your Files
====================

Before running the server, you need some files to serve. All files must be in
the `root`_ directory and its sub-directories. In fact, an error will occur if a
file is requested outside of the ``root`` directory. The ``root`` directory can
exist anywhere on your filesystem as long as Rheostatic has permission to read
the files.

Ensure that all files are saved using the same encoding and that that encoding
is being used by Rheostatic. See `encoding`_ for details.

A file's ContentType is determined by its file extension. For best results, use
common file extensions for your files. A list of known file extensions and the
ContentType used for each can be found in `rheostatic/utils.py`_.

.. _rheostatic/utils.py: https://github.com/waylan/rheostatic/blob/master/rheostatic/utils.py#L100

If you would like a file to be served when the client requests a directory (for
example ``/``, or ``/path/to/some/dir/``), then that directory needs to contain an
index file. Be sure to use the file name for the index file set by the
`index_file`_ option. The default for most servers (including Rheostatic) is
``index.html``.

If a directory does not contain an index file, then Rheostatic will return a
directory listing of all the files in that directory (excluding files with names
that start with a dot).

For custom error pages, include files in the "root" directory named
``<code>.html`` where ``<code>`` is the HTTP error code which the error page
corresponds to. For example, a file named ``404.html`` would be returned for
``404`` (Not Found) errors. Supported error codes include ``404`` (Not Found),
and ``405`` (Method Not Allowed). If a custom error page is not found, then
Rheostatic serves a simple plain-text error page.

Options
=======

Rheostatic currently supports the following options:

root
----

The local file system directory which the server should use as its "root"
directory. Usually represented by ``/`` in the URL (for example
``http://example.com/``). When ``root`` is set to a relative path, the local
filesystem path is resolved as an absolute path relative to the current working
directory. Absolute paths are used as-is.

index_file
----------

The name of the file returned when a directory is requested (a URL ending with a
``/``). A file by that name must be present in the requested directory. Defaults
to ``index.html``.

For example, a request to ``/`` would return the file at ``/index.html`` without
redirecting the client.

default_type
------------

The ContentType returned for a file when the type is unknown. Defaults to
``application/octet-stream``.

encoding
--------

The encoding used to read and serve the files. Be sure all your files are saved
using the same encoding. Defaults to ``utf-8``.

directory_template
------------------

An HTML template used to display a directory listing when no index file is
available for the requested directory. Defaults to the string defined at
``utils.directory_template``.

default_extension
-----------------

The extension to use for extensionless URLs. The requested URL must not end in
an extension or a slash (``/``). This feature is disabled by default. To enable
the feature, set the option to a string which contains both a dot and the
desired extension. For example, with the option set to ``.html``, a request to
``/foo`` would return the file ``/foo.html`` without redirecting the client.

Infrequently Asked Questions
============================

Why Does this Exist?
--------------------

The existing solutions have different goals and do not offer the specific set of
features that I needed. While some libraries could be subclassed to alter the
behavior, attempts to provide patches upstream always result in rejection as the
libraries generally where intended to serve static *support* files (images, CSS
files, JavaScript, etc), specifically to support dynamic content (cgi, wsgi,
Django, etc.). However, I needed to serve a static site; specifically static
HTML files along with their supporting media files (generated from a static site
generator). I can't trust that the existing solutions will continue to work, as
their goals do not align with my needs.

On the other hand, other simple servers often don't offer enough features to
emulate a real server. Thus, Rheostatic was created to offer the flexibility and
features to meet all of the needs of static site generators.

Why is it called "Rheostatic"?
------------------------------

I wanted something that accurately conveyed the purpose and function of the
library/tool. Note that the similar word, "rheostat" comes from the Greek
"rheos" (stream) and is `defined`_ as "[a]n electrical instrument used to
control a current by varying the resistance." Rheostatic doesn't control
current, but it does control a *stream* of *static* files served to a client,
which can be varied by adjusting the settings. I also liked the name and it
doesn't appear to have been used by anyone else.

.. _defined: https://en.oxforddictionaries.com/definition/us/rheostat

Could you add my pet feature?
-----------------------------

Maybe. If the feature does not add support for dynamic content and it can be
easily replicated by popular web servers, I may consider it. Naturally, if you
do the work it's more likely to get added, than if you wait for me to work on
something I don't care about and/or need.

License
=======

Rheostatic is licensed under the `MIT License`_ as defined in `LICENSE`.

.. _MIT License: https://opensource.org/licenses/MIT

Change Log
==========

Version 0.0.2 (2020-10-27)
--------------------------

* Added support for `text/cache-manifest` content type.
* Dropped support for Python versions less that 3.6.

Version 0.0.1 (2016-11-03)
--------------------------

The initial release.
