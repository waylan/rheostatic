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


# version_info should conform to PEP 386
# (major, minor, micro, alpha/beta/rc/final, #)
# (1, 1, 2, 'alpha', 0) => "1.1.2.dev"
# (1, 2, 0, 'beta', 2) => "1.2b2"
__version_info__ = (0, 0, 2, 'final', 0)


def _get_version():  # pragma: no cover
    " Returns a PEP 386-compliant version number from version_info. "
    assert len(__version_info__) == 5
    assert __version_info__[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if __version_info__[2] == 0 else 3
    main = '.'.join(map(str, __version_info__[:parts]))

    sub = ''
    if __version_info__[3] == 'alpha' and __version_info__[4] == 0:
        # TODO: maybe append some sort of git info here??
        sub = '.dev'
    elif __version_info__[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[__version_info__[3]] + str(__version_info__[4])

    return str(main + sub)


__version__ = _get_version()


# Follow Django in treating URLs as UTF-8 encoded (which requires undoing the
# implicit ISO-8859-1 decoding applied in Python 3). Strictly speaking, URLs
# should only be ASCII anyway, but UTF-8 can be found in the wild.
def decode_path_info(path_info):
    return path_info.encode('iso-8859-1').decode('utf-8')


# Define only the HTTP status codes we actually use
http_status = {
    200: 'OK',
    301: 'Moved Permanently',
    304: 'Not Modified',
    404: 'Not Found',
    405: 'Method Not Allowed'

}

directory_template = """<!DOCTYPE html>
<html>
    <head>
        <title>Directory listing for {displaypath}</title>
    </head>
    <body>
        <h2>Directory listing for {displaypath}</h2>
        <hr>
        <ul>
            {items}
        </ul>
        <hr>
    </body>
</html>
""".replace('\n', os.linesep)

# Define our own types for consistency cross platform.
# Use the types defined by nginx with a few additions.
types_map = {
    '.3gp': 'video/3gpp',
    '.3gpp': 'video/3gpp',
    '.7z': 'application/x-7z-compressed',
    '.ai': 'application/postscript',
    '.asf': 'video/x-ms-asf',
    '.asx': 'video/x-ms-asf',
    '.atom': 'application/atom+xml',
    '.avi': 'video/x-msvideo',
    '.bmp': 'image/x-ms-bmp',
    '.cco': 'application/x-cocoa',
    '.crt': 'application/x-x509-ca-cert',
    '.css': 'text/css',
    '.der': 'application/x-x509-ca-cert',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.ear': 'application/java-archive',
    '.eot': 'application/vnd.ms-fontobject',
    '.eps': 'application/postscript',
    '.flv': 'video/x-flv',
    '.gif': 'image/gif',
    '.hqx': 'application/mac-binhex40',
    '.htc': 'text/x-component',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.ico': 'image/x-icon',
    '.jad': 'text/vnd.sun.j2me.app-descriptor',
    '.jar': 'application/java-archive',
    '.jardiff': 'application/x-java-archive-diff',
    '.jng': 'image/x-jng',
    '.jnlp': 'application/x-java-jnlp-file',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.kar': 'audio/midi',
    '.kml': 'application/vnd.google-earth.kml+xml',
    '.kmz': 'application/vnd.google-earth.kmz',
    '.m3u8': 'application/vnd.apple.mpegurl',
    '.m4a': 'audio/x-m4a',
    '.m4v': 'video/x-m4v',
    '.manifest': 'text/cache-manifest',
    '.mid': 'audio/midi',
    '.midi': 'audio/midi',
    '.mml': 'text/mathml',
    '.mng': 'video/x-mng',
    '.mov': 'video/quicktime',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4',
    '.mpeg': 'video/mpeg',
    '.mpg': 'video/mpeg',
    '.ogg': 'audio/ogg',
    '.pdb': 'application/x-pilot',
    '.pdf': 'application/pdf',
    '.pem': 'application/x-x509-ca-cert',
    '.pl': 'application/x-perl',
    '.pm': 'application/x-perl',
    '.png': 'image/png',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.prc': 'application/x-pilot',
    '.ps': 'application/postscript',
    '.ra': 'audio/x-realaudio',
    '.rar': 'application/x-rar-compressed',
    '.rpm': 'application/x-redhat-package-manager',
    '.rss': 'application/rss+xml',
    '.rtf': 'application/rtf',
    '.run': 'application/x-makeself',
    '.sea': 'application/x-sea',
    '.shtml': 'text/html',
    '.sit': 'application/x-stuffit',
    '.svg': 'image/svg+xml',
    '.svgz': 'image/svg+xml',
    '.swf': 'application/x-shockwave-flash',
    '.tcl': 'application/x-tcl',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.tk': 'application/x-tcl',
    '.ts': 'video/mp2t',
    '.txt': 'text/plain',
    '.war': 'application/java-archive',
    '.wbmp': 'image/vnd.wap.wbmp',
    '.webm': 'video/webm',
    '.webp': 'image/webp',
    '.wml': 'text/vnd.wap.wml',
    '.wmlc': 'application/vnd.wap.wmlc',
    '.wmv': 'video/x-ms-wmv',
    '.woff': 'application/font-woff',
    '.woff2': 'font/woff2',
    '.xhtml': 'application/xhtml+xml',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xml': 'text/xml',
    '.xpi': 'application/x-xpinstall',
    '.xspf': 'application/xspf+xml',
    '.zip': 'application/zip'
}
