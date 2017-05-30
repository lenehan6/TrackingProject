import SimpleHTTPServer
import SocketServer
import threading
import json

from PyQt4.QtCore import *


class WebServer(QThread):
    def __init__(self, app, parent=None):
        QThread.__init__(self, parent);
        self.HOST = "localhost"
        self.PORT = 8084
        self.Handler = '';
        self.httpd = '';
        self._quit = False;
        self.app = app;

    def createServer(self, host, port, handler):
        try:
            server = SocketServer.TCPServer((host, port), handler);
        except:
            server = self.createServer(host, port + 1, handler);

        return server;

    def run(self):
        self.Handler = Handler;
        self.Handler.app = self.app;
        self.httpd = self.createServer(self.HOST, self.PORT, self.Handler)
        print "serving at port", self.PORT

        while not self._quit:
            try:
                self.httpd.serve_forever();
            finally:
                break;

        print "WebServer closed"

    def quit(self):
        self._quit = True;
        self.httpd.shutdown();
        self.httpd.server_close();


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        #print "%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args);
        return;

    def do_GET(self):
        if (str(self.path).startswith("/api/")):
            self.apiHandler(self.path);
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def apiHandler(self, path):
        path = path.replace("/api/", "");
        p = path.split("/");

        if (len(p) == 0):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            return;

        if (p[0] == "locations"):
            if (p[1] == "get"):
                self.send_response(200, "OK");
                self.send_header("Content-type", "application/json")
                self.end_headers()

                _out = [];
                for d in self.app.devices:
                    _device = dict();
                    _device["name"] = d.name;
                    _device["details"] = d.lastPosition.dict()
                    _out.append( _device );

                self.wfile.write(json.dumps(_out));
                return;
        elif (p[0] == "course"):
            if (p[1] == "get"):
                self.send_response(200, "OK");
                self.send_header("Content-type", "application/vnd.google-earth.kml+xml")
                self.end_headers()
                self.wfile.write( self.app.event.course.file );
                return;

        self.send_response(404, "API request does not exist");
