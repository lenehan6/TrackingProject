import json
import re

import time

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn
import threading
import requests

import numpy

from PyQt5.QtCore import *

#define
REGEX_EVENTLINK = "\/[0-9]{5}(\/$)?(\/.+)?$"



class WebServer(threading.Thread):
    def __init__(self, app, parent=None):
        QThread.__init__(self, parent);
        self.HOST = "localhost"
        self.PORT = 8080
        self.Handler = '';
        self.httpd = '';
        self._quit = False;
        self.app = app;
        self.db = '';
        self.portForEvent = {12345: 8081};
        self.error = dict();

    def __del__(self):
        self._quit = True;

    def setDatabase(self, db):
        self.db = db;

    def createServer(self, host, port, handler):
        try:
            server = ThreadedHTTPServer((host, port), handler);
        except:
            server = self.createServer(host, port + 1, handler);

        return server;

    def run(self):
        self.Handler = Handler;
        self.Handler.app = self.app;
        self.Handler.db = self.db;
        self.Handler.portForEvent = self.portForEvent;
        self.httpd = self.createServer(self.HOST, self.PORT, self.Handler)
        print "serving at port", self.PORT

        try:
            self.httpd.serve_forever();
        except Exception, e:
            exception_name, exception_value = sys.exc_info()[:2]
            self.error["err"] = exception_value;
            self.error["error"] = exception_name;
        finally:
            self.quit();

        self.quit();
        print "WebServer closed"

    def quit(self):
        self._quit = True;
        self.httpd.shutdown();
        self.httpd.server_close();

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print "%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args);
        return;

    def do_GET(self):
        #tick = time.time();

        if (str(self.path).startswith("/api/")):
            self.apiHandler(self.path);
        elif ( re.match( self.path, REGEX_EVENTLINK ) ):
            event = int(self.path[1:5]);
            if event in self.portForEvent:
                eventPort = self.portForEvent[event];
                self.path = self.path[6:];
                r = requests.get( "localhost:" + str(eventPort) + "/" + self.path, port=eventPort);
                self.send_response( r.status_code, "OK");
                self.send_header("Content-type", r.headers["Content-type"]);
                self.end_headers()
                self.wfile.write( r.text );
            else:
                self.send_response(404, "Event not found");
                self.end_headers();

        else:
            SimpleHTTPRequestHandler.do_GET(self)

        #qDebug( threading.currentThread().getName() );

        #print "'" + self.path + "' took " + str(int((time.time() - tick) * 1E6)) + "us";

    def do_POST(self):
        #tick = time.time();

        if (str(self.path).startswith("/api/")):
            self.apiHandler(self.path);
        elif (re.match(self.path, REGEX_EVENTLINK)):
            event = int(self.path[1:5]);
            if event in self.portForEvent:
                eventPort = int(self.portForEvent[event]);
                self.path = self.path[6:];
                r = requests.post("localhost:" + str(eventPort) + "/" + self.path, self.rfile.readAll());
                self.send_response(r.status_code, "OK");
                self.send_header("Content-type", r.headers["Content-type"]);
                self.end_headers()
                self.wfile.write(r.text);
            else:
                self.send_response(404, "Event not found");
                self.end_headers();
        else:
            SimpleHTTPRequestHandler.do_POST(self)

        #print "'" + self.path + "' took " + str(int((time.time() - tick) * 1E6)) + "us";


    def apiHandler(self, path):

        path = path.replace("/api/", "");

        pathSplit = path.split("?");
        p = pathSplit[0].split("/");

        getParams = dict();
        if ( len(pathSplit) > 1 ):
            for param in pathSplit[1].split("&"):
                x = param.split("=");
                if ( len(x) == 2 ):
                    if ( x[0] != "" ) and ( x[1] != "" ):
                        getParams[ x[0] ] = x[1];

        if (len(p) == 0):
            SimpleHTTPRequestHandler.do_GET(self)
            return;


        self.send_response(404, "API request does not exist");
