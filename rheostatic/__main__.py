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

import os
import argparse

from . import serve, __version__


def parse_args(*args):
    parser = argparse.ArgumentParser(prog='rheostatic',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Rheostatic - A Static File Server with options.')
    parser.add_argument('root', default='.', nargs='?', help='set the root directory of the server')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__version__,
                        help='show the current version and exit')
    parser.add_argument('-o', '--host', default='localhost',
                        help='set the host (or IP address) of the server')
    parser.add_argument('-p', '--port', default='8000', type=int,
                        help='set the port of the server')
    parser.add_argument('-i', '--index-file', default='index.html', metavar='FILENAME',
                        help='set the filename to use for index files')
    parser.add_argument('-t', '--default-type', default='application/octet-stream', metavar='TYPE',
                        help='set the ContentType with which files of an unknown type are served')
    parser.add_argument('-e', '--encoding', default='utf-8',
                        help='set the encoding with which all files are served')
    parser.add_argument('-x', '--default-extension', default=argparse.SUPPRESS, metavar='.EXT',
                        help='set the default extension to append to URLs')
    # A hidden argument for testing purposes.
    # When set, uses the `rheostatic/tests/data/` dir as root
    parser.add_argument('--test', action='store_true', default=argparse.SUPPRESS,
                        help=argparse.SUPPRESS)

    args = vars(parser.parse_args(*args))

    address = (args.pop('host'), args.pop('port'))
    root = args.pop('root')
    if 'test' in args:                                      # pragma: no cover
        args.pop('test')
        root = os.path.join(os.path.dirname(__file__), 'tests/data/')

    return address, root, args


def cli():                                                  # pragma: no cover
    address, root, args = parse_args()
    serve(address, root, **args)


if __name__ == '__main__':                                  # pragma: no cover
    cli()
