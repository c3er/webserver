#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import threading
import optparse
import http.server


DEFAULT_PORT = 3030


# HTTP related #################################################################

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """A cludge to accomplish an easy way to serve another directory than the
    current one.
    """
    root_path = ''

    def __init__(self, *args, **kw):
        self.__path = ''
        super().__init__(*args, **kw)

    def _get_path(self):
        path, file = os.path.split(self.__path)
        fullpath = os.path.join(path, self.root_path, file).replace('\\', '/')
        print(fullpath)
        return fullpath

    def _set_path(self, val):
        self.__path = val

    path = property(_get_path, _set_path)


class HTTPServerWorker(threading.Thread):
    def __init__(self, port, root_path):
        super().__init__()
        HTTPRequestHandler.root_path = root_path
        self.httpd = http.server.HTTPServer(("", port), HTTPRequestHandler)

    def run(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()

################################################################################


# Helper functions #############################################################

def get_option_count(options):
    opt_count = 0
    for val in options.__dict__.values():
        if val is not None:
            opt_count += 1
    return opt_count


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option(
        '-p',
        '--port',
        dest='port',
        help='Serverport. Default port is ' + str(DEFAULT_PORT)
    )
    parser.add_option(
        '-r',
        '--root',
        dest='root_path',
        help='Root path. The default root path is the current directory.'
    )
    options, args = parser.parse_args()  # "args" not needed here
    return parser, options

################################################################################


def main():
    # Evaluate given options ###################################################
    parser, options = parse_args()
    if get_option_count(options) == 0:
        parser.print_help()

    if options.port:
        portstr = options.port
        try:
            port = int(portstr)
        except ValueError as exc:
            parser.error(f'Could not identify "{portstr}" as port.')
    else:
        port = DEFAULT_PORT

    if options.root_path:
        root_path = options.root_path
        if not os.path.isdir(root_path):
            parser.error(f'Given path "{root_path}" does not lead to a directory.')
        if len(root_path) > 0 and not root_path.endswith('/'):
            root_path += '/'
    else:
        root_path = ''
    ############################################################################

    httpd = HTTPServerWorker(port, root_path)

    print(
        f'Serving at port {port} with root path "{root_path}"',
        f'http://localhost:{port}/',
        'Press Enter to exit.',
        sep='\n'
    )
    httpd.start()

    input()
    print('Exiting')
    httpd.shutdown()


if __name__ == '__main__':
    main()
