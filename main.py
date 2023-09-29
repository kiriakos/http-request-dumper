#!/usr/bin/env python3
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import time_ns
import pathlib



class RequestHandler(BaseHTTPRequestHandler):

    flat_files = False

    def get_content(self):
        ct_header = self.headers.get('Content-Length')
        if (ct_header is not None) and (len(ct_header) > 0):
          content_length = int(self.headers.get('Content-Length', 0))
          return self.rfile.read(content_length).decode('utf-8')
        else:
          return None

    def write_file(self, content):

        path_slug=self.path.split("?")[0]
        if self.flat_files:
          directory = "/requests"
        else:
          directory = f'/requests/{path_slug}'
          pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        ts = time_ns()
        file=f'{directory}/{ts}_{self.command}.http'

        f = open(file, "a")
        f.write(f'{self.command} {self.path}\n')

        for header in self.headers:
            value = self.headers[header]
            f.write(f'{header}: {value}\n')
        f.write("\n")

        if content is not None:
          f.write(content)

        f.close()

    def handle_request(self):
        content = self.get_content()

        self.write_file(content)

        print("----- Request Start ----->")
        self.print_header()
        if content is not None:
          print("Payload:")
          print(content)
        print("<----- Request End -----\n")

        self.send_response(200)
        self.end_headers()

    def print_header(self):
        self.print_detail('Method', self.command)
        self.print_detail('Path', self.path)
        self.print_headers()
        print()

    @property
    def column_width(self):
        max_key_length = max([len(key) for key in self.headers.items()])
        width = max_key_length + 2
        return width

    def print_headers(self):
        for key in sorted(self.headers):
            value = self.headers[key]
            self.print_detail(key, value)

    def print_detail(self, label, value):
        label += ': '
        entry = '{}{}'.format(label.ljust(self.column_width), value)
        print(entry)

    do_GET     = handle_request
    do_HEAD    = handle_request
    do_OPTIONS = handle_request
    do_DELETE  = handle_request

    do_POST    = handle_request
    do_PUT     = handle_request
    do_PATCH   = handle_request


def run_server(address, port):
    server_address = (address, int(port))
    print('Listening on {}'.format(server_address))
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()


if __name__ == "__main__":

    parser = OptionParser()
    parser.usage = "Creates a HTTP server for debugging purposes"

    parser.add_option("-a", "--address", dest="listen_address",
                      default='0.0.0.0', help="HTTP listen address")
    parser.add_option("-p", "--port", dest="listen_port",
                      default=8080, help="HTTP listen port")
    parser.add_option("-f", "--flat", dest="flat",
                      action="store_true", help="Create flat files instead of a directory structure")

    (options, args) = parser.parse_args()
    if options.flat:
        RequestHandler.flat_files = True
    print("Starting server")
    run_server(options.listen_address, options.listen_port)
