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
import io
import posixpath
import wsgiref
from email import utils as rfc822
from urllib.parse import unquote as urlunquote
from urllib.parse import quote as urlquote
from html import escape as html_escape
from . import utils


class Rheostatic:
    """
    Static File Server with options.

    Serve static files from the given root directory and any subdirectories.
    Responds to GET and HEAD requests.

    """

    server_version = 'rheostatic/' + utils.__version__
    index_file = 'index.html'
    default_extension = None
    default_type = 'application/octet-stream'
    encoding = 'utf-8'
    directory_template = utils.directory_template

    def __init__(self, root, **kwargs):
        self.root = os.path.abspath(root)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, environ, start_response):
        """ Send the response code and MIME headers. """
        if environ['REQUEST_METHOD'] not in ('GET', 'HEAD'):
            # Unsupported method
            headers = [('Allow', 'GET, HEAD')]
            return self.error(405, environ, start_response, headers)

        path_info = environ.get('PATH_INFO', '')
        path = self.get_full_path(path_info)

        if not path.startswith(self.root):              # pragma: no cover
            # Outside server root
            return self.error(404, environ, start_response)

        if os.path.isdir(path):
            if not path_info.endswith('/'):
                # Dir does not end with /, redirect
                location = wsgiref.util.request_uri(environ, include_query=False) + '/'
                if environ.get('QUERY_STRING'):
                    location += '?' + environ.get('QUERY_STRING')  # pragma: no cover
                headers = [('Location', location)]
                return self.simple_error(301, environ, start_response, headers)
            index = os.path.join(path, self.index_file)
            if os.path.isfile(index):
                path = index
            else:
                return self.list_directory(path, environ, start_response)

        if os.path.isfile(path):
            try:
                file_stat = os.stat(path)
                headers = [
                    ('Date', rfc822.formatdate(usegmt=True)),
                    ('Last-Modified', rfc822.formatdate(file_stat.st_mtime, usegmt=True)),
                    ('Content-Length', str(file_stat.st_size)),
                    ('Content-type', '{}; charset={}'.format(self.guess_type(path),
                                                             self.encoding))
                ]
                # TODO: add support for HTTP_IF_MODIFIED_SINCE and HTTP_IF_NONE_MATCH
                start_response(self.get_status(200), headers)
                return self.get_body(path, environ)
            except OSError:                  # pragma: no cover
                return self.error(404, environ, start_response)

        return self.error(404, environ, start_response)

    def get_full_path(self, path_info):
        """ Get local filename path from path_info. """
        path_info = utils.decode_path_info(path_info)
        path_info = posixpath.normpath(urlunquote(path_info))
        path = os.path.normpath(self.root + path_info)
        if (self.default_extension and
                not os.path.exists(path) and
                os.path.splitext(path)[1] == '' and
                os.path.isfile(path + self.default_extension)):
            path += self.default_extension
        return path

    def get_status(self, code):
        return '%d %s' % (code, utils.http_status[code])

    def get_body(self, path, environ):
        if environ['REQUEST_METHOD'] == 'HEAD':
            return [b'']
        else:
            file_wrapper = environ.get('wsgi.file_wrapper', wsgiref.util.FileWrapper)
            return file_wrapper(open(path, 'rb'))

    def guess_type(self, path):
        extension = os.path.splitext(path)[1].lower()
        return utils.types_map.get(extension, self.default_type)

    def error(self, code, environ, start_response, headers=None):
        """
        Send an error reply.

        If an error page exists at the server root in the format [code].html,
        then that page is returned instead of the message.

        """
        headers = headers or []
        path = os.path.join(self.root, f'{code}.html')
        if os.path.isfile(path):
            try:
                file_stat = os.stat(path)
                headers.extend([
                    ('Content-Length', str(file_stat.st_size)),
                    ('Content-type', '{}; charset={}'.format(self.guess_type(path),
                                                             self.encoding))
                ])
                start_response(self.get_status(code), headers)
                return self.get_body(path, environ)
            except OSError:                  # pragma: no cover
                return self.simple_error(code, environ, start_response, headers)
        else:
            return self.simple_error(code, environ, start_response, headers)

    def simple_error(self, code, environ, start_response, headers=None):
        """ Send a plain text error. """
        headers = headers or []
        status = self.get_status(code)
        headers.extend([
            ('Content-Length', str(len(status))),
            ('Content-type', f'text/plain; charset={self.encoding}')
        ])
        start_response(status, headers)
        return [status.encode(self.encoding)]

    def list_directory(self, path, environ, start_response):
        """ Return a directory listing. """
        try:
            names = os.listdir(path)
        except os.error:                                # pragma: no cover
            return self.error(404, environ, start_response)
        names.sort(key=lambda a: a.lower())

        items = []
        for name in names:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            items.append('<li><a href="{}">{}</a></li>'.format(
                urlquote(linkname), html_escape(displayname)
            ))

        f = io.BytesIO()
        f.write(self.directory_template.format(
            displaypath=html_escape(urlunquote(wsgiref.util.request_uri(environ))),
            items=os.linesep.join(items)
        ).encode(self.encoding))
        length = f.tell()
        f.seek(0)

        headers = [
            ('Content-Length', str(length)),
            ('Content-type', f'text/html; charset={self.encoding}')
        ]
        start_response(self.get_status(200), headers)
        file_wrapper = environ.get('wsgi.file_wrapper', wsgiref.util.FileWrapper)
        return file_wrapper(f)
