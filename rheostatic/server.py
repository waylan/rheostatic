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

from wsgiref.validate import validator
from wsgiref.simple_server import make_server

from .base import Rheostatic


def serve(address, root, **kwargs):                     # pragma: no cover
    """ Serve static files from root directory. """

    app = Rheostatic(root, **kwargs)

    server = make_server(address[0], address[1], validator(app))

    try:
        print('Starting server at http://%s:%d/...' % address)
        print('Serving files from %s' % app.root)
        print('Press ctrl+c to stop.')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Quiting...')
