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

from unittest import TestCase

from rheostatic.__main__ import parse_args


class TestCli(TestCase):

    def test_default_args(self):
        self.assertEqual(
            parse_args([]),
            (
                ('localhost', 8000),
                '.',
                {
                    'index_file': 'index.html',
                    'default_type': 'application/octet-stream',
                    'encoding': 'utf-8'
                }
            )
        )

    def test_root_arg(self):
        self.assertEqual(
            parse_args(['some/path/']),
            (
                ('localhost', 8000),
                'some/path/',
                {
                    'index_file': 'index.html',
                    'default_type': 'application/octet-stream',
                    'encoding': 'utf-8'
                }
            )
        )

    def test_host_arg(self):
        self.assertEqual(
            parse_args(['--host', '0.0.0.0']),
            (
                ('0.0.0.0', 8000),
                '.',
                {
                    'index_file': 'index.html',
                    'default_type': 'application/octet-stream',
                    'encoding': 'utf-8'
                }
            )
        )

    def test_port_arg(self):
        self.assertEqual(
            parse_args(['--port', '80']),
            (
                ('localhost', 80),
                '.',
                {
                    'index_file': 'index.html',
                    'default_type': 'application/octet-stream',
                    'encoding': 'utf-8'
                }
            )
        )

    def test_index_file_arg(self):
        self.assertEqual(
            parse_args(['--index-file', 'README']),
            (
                ('localhost', 8000),
                '.',
                {
                    'index_file': 'README',
                    'default_type': 'application/octet-stream',
                    'encoding': 'utf-8'
                }
            )
        )

    def test_default_type_arg(self):
        self.assertEqual(
            parse_args(['--default-type', 'text/plain']),
            (
                ('localhost', 8000),
                '.',
                {
                    'index_file': 'index.html',
                    'default_type': 'text/plain',
                    'encoding': 'utf-8'
                }
            )
        )

    def test_encoding_arg(self):
        self.assertEqual(
            parse_args(['--encoding', 'ASCII']),
            (
                ('localhost', 8000),
                '.',
                {
                    'index_file': 'index.html',
                    'default_type': 'application/octet-stream',
                    'encoding': 'ASCII'
                }
            )
        )

    def test_default_extension_arg(self):
        self.assertEqual(
            parse_args(['--default-extension', '.html']),
            (
                ('localhost', 8000),
                '.',
                {
                    'index_file': 'index.html',
                    'default_type': 'application/octet-stream',
                    'encoding': 'utf-8',
                    'default_extension': '.html'
                }
            )
        )
