import http.server
import socketserver
import atexit
import webbrowser

from skyutils.logger import Logger


class Webserver:
    def __init__(self):
        self.ip = -1
        self.port = -1

    # TODO: Implement BaseHTTPRequestHandler with request handler
    def start(self, debug):
        logger = Logger(True)

        class quietServer(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                if debug:
                    msg = f'{self.address_string()} {format%args} \n'
                    logger.webserver.info(msg)
                else:
                    pass

        with socketserver.TCPServer(("127.0.0.1", 0), quietServer) as httpd:
            self.ip = httpd.socket.getsockname()[0]
            self.port = httpd.socket.getsockname()[1]
            atexit.register(self.close_skyspy, httpd)
            print("webserver started")
            print(httpd.socket.getsockname())
            webbrowser.open_new_tab(
                f"http://localhost:{self.port}/web/skyspy.html")
            httpd.serve_forever()

    def close_skyspy(self, httpd):
        httpd.shutdown()
        print("closing skyspy")
