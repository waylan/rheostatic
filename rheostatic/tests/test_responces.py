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
from unittest import TestCase
from wsgi_intercept import (
    http_client_intercept, add_wsgi_intercept, remove_wsgi_intercept
)
import http.client as http_lib
from rheostatic.base import Rheostatic

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def make_app(**kwargs):
    def wrapper():
        return Rheostatic(ROOT, **kwargs)
    return wrapper


def get_file_content(path):
    with open(os.path.join(ROOT, path), 'rb') as f:
        return f.read()


class TestResponses(TestCase):
    def assertResponse(self, app, method, url, status=None, headers=None, content=None):
        host, port = 'localhost', 80
        http_client_intercept.install()
        add_wsgi_intercept(host, port, app)
        client = http_lib.HTTPConnection(host, port)
        client.request(method, url)
        response = client.getresponse()

        if status is not None:
            self.assertEqual(response.status, status)

        headers = headers or {}
        for k, v in headers.items():
            self.assertEqual(response.getheader(k), v)

        if content is not None:
            self.assertEqual(response.read(), content)

        client.close()
        remove_wsgi_intercept(host, port)
        http_client_intercept.uninstall()

    def test_get_homepage(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('index.html')
        )

    def test_head_homepage(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_other_page(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/other.html',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('other.html')
        )

    def test_head_other_page(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/other.html',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_subpage(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/subdir/subpage.html',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('subdir/subpage.html')
        )

    def test_head_subpage(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/subdir/subpage.html',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_image(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/favicon.ico',
            status=200,
            headers={'Content-type': 'image/x-icon; charset=utf-8'},
            content=get_file_content('favicon.ico')
        )

    def test_head_image(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/favicon.ico',
            status=200,
            headers={'Content-type': 'image/x-icon; charset=utf-8'},
            content=b''
        )

    def test_get_default_type(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/subdir/unknown-file-type.abc',
            status=200,
            headers={'Content-type': 'application/octet-stream; charset=utf-8'},
            content=get_file_content('subdir/unknown-file-type.abc')
        )

    def test_head_default_type(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/subdir/unknown-file-type.abc',
            status=200,
            headers={'Content-type': 'application/octet-stream; charset=utf-8'},
            content=b''
        )

    def test_get_dir_listing(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/subdir/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('subdir/expected_dir_list.html')
        )

    def test_head_dir_listing(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/subdir/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_redirect(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/subdir',
            status=301,
            headers={
                'Location': 'http://localhost/subdir/',
                'Content-type': 'text/plain; charset=utf-8'
            },
            content=b'301 Moved Permanently'
        )

    def test_head_redirect(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/subdir',
            status=301,
            headers={
                'Location': 'http://localhost/subdir/',
                'Content-type': 'text/plain; charset=utf-8'
            },
            content=b''
        )

    def test_unsupported_method(self):
        self.assertResponse(
            app=make_app(),
            method='POST',
            url='/',
            status=405,
            headers={
                'Allow': 'GET, HEAD',
                'Content-type': 'text/plain; charset=utf-8'
            },
            content=b'405 Method Not Allowed'
        )

    def test_get_not_found(self):
        self.assertResponse(
            app=make_app(),
            method='GET',
            url='/nonexistant.html',
            status=404,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('404.html')
        )

    def test_head_not_found(self):
        self.assertResponse(
            app=make_app(),
            method='HEAD',
            url='/nonexistant.html',
            status=404,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_default_extension(self):
        self.assertResponse(
            app=make_app(default_extension='.html'),
            method='GET',
            url='/other',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('other.html')
        )

    def test_head_default_extension(self):
        self.assertResponse(
            app=make_app(default_extension='.html'),
            method='HEAD',
            url='/other',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_custom_index(self):
        self.assertResponse(
            app=make_app(index_file='other.html'),
            method='GET',
            url='/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=get_file_content('other.html')
        )

    def test_head_custom_index(self):
        self.assertResponse(
            app=make_app(index_file='other.html'),
            method='HEAD',
            url='/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_custom_encoding(self):
        self.assertResponse(
            app=make_app(encoding='ascii'),
            method='GET',
            url='/',
            status=200,
            headers={'Content-type': 'text/html; charset=ascii'},
            content=get_file_content('index.html')
        )

    def test_head_custom_encoding(self):
        self.assertResponse(
            app=make_app(encoding='ascii'),
            method='HEAD',
            url='/',
            status=200,
            headers={'Content-type': 'text/html; charset=ascii'},
            content=b''
        )

    def test_get_custom_dir_listing(self):
        template = 'A replacement template'
        self.assertResponse(
            app=make_app(directory_template=template),
            method='GET',
            url='/subdir/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=template.encode('utf-8')
        )

    def test_head_custom_dir_listing(self):
        template = 'A replacement template'
        self.assertResponse(
            app=make_app(directory_template=template),
            method='HEAD',
            url='/subdir/',
            status=200,
            headers={'Content-type': 'text/html; charset=utf-8'},
            content=b''
        )

    def test_get_custom_default_type(self):
        self.assertResponse(
            app=make_app(default_type='text/plain'),
            method='GET',
            url='/subdir/unknown-file-type.abc',
            status=200,
            headers={'Content-type': 'text/plain; charset=utf-8'},
            content=get_file_content('subdir/unknown-file-type.abc')
        )

    def test_head_custom_default_type(self):
        self.assertResponse(
            app=make_app(default_type='text/plain'),
            method='HEAD',
            url='/subdir/unknown-file-type.abc',
            status=200,
            headers={'Content-type': 'text/plain; charset=utf-8'},
            content=b''
        )
