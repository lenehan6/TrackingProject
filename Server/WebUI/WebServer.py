import SimpleHTTPServer
import SocketServer
import threading
import json
import time

import numpy

from PyQt5.QtCore import *


class WebServer(QThread):
    def __init__(self, app, parent=None):
        QThread.__init__(self, parent);
        self.HOST = "localhost"
        self.PORT = 8093
        self.Handler = '';
        self.httpd = '';
        self._quit = False;
        self.app = app;
        self.db = '';

    def __del__(self):
        self._quit = True;

    def setDatabase(self, db):
        self.db = db;

    def createServer(self, host, port, handler):
        try:
            server = SocketServer.TCPServer((host, port), handler);
        except:
            server = self.createServer(host, port + 1, handler);

        return server;

    def run(self):
        self.Handler = Handler;
        self.Handler.app = self.app;
        self.Handler.db = self.db;
        self.httpd = self.createServer(self.HOST, self.PORT, self.Handler)
        print "serving at port", self.PORT

        while not self._quit:
            try:
                self.httpd.serve_forever();
            finally:
                break;

        self.quit();
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
        #tick = time.time();

        if (str(self.path).startswith("/api/")):
            self.apiHandler(self.path);
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        #print "'" + self.path + "' took " + str(int((time.time() - tick) * 1E6)) + "us";

    def do_POST(self):
        #tick = time.time();

        if (str(self.path).startswith("/api/")):
            self.apiHandler(self.path);
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST(self)

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
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            return;

        if (p[0] == "locations"):
            if (p[1] == "get"):
                self.send_response(200, "OK");
                self.send_header("Content-type", "application/json")
                self.end_headers()

                query = "SELECT * FROM stage1.apiCache WHERE key='gapTime/get'";
                q = self.db.do_query(query);

                gap = dict();
                while q.next():
                    if q.value("key") == "gapTime/get":
                        qDebug( q.value("value") );
                        gap = json.loads( q.value("value") );

                _out = [];
                for d in self.app.devices:
                    _device = dict();
                    _device["id"] = d.id;
                    _device["name"] = d.name;
                    _device["speed"] = numpy.round( d.speed*3.6, 1 );
                    _device["distance"] = numpy.round( d.distance / 1000, 1 );
                    _device["isEnabled"] = d.isEnabled;
                    _device["details"] = d.lastPosition.dict();
                    if d.addr in gap:
                        _device["gap"] = gap[ d.addr ];
                    else:
                        _device["gap"] = -1;

                    _out.append( _device );

                self.wfile.write(json.dumps(_out));
                return;

            elif (p[1] == "set"):
                qDebug( self.path );
                self.send_response(200, "OK");
                self.send_header("Content-type", "application/json")
                self.end_headers();

                data = json.loads( self.rfile.read( int(self.headers.getheader('Content-length')) ) );


                if "data" not in data:
                    self.wfile.write(json.dumps({"error": "Missing `data` parameter"}));
                    return;

                data = list(data["data"]);

                for d in self.app.devices:
                    if d.id == int( data["id"] ):
                        if "isEnabled" in getParams:
                            d.isEnabled = (getParams["isEnabled"]=="true");
                            qDebug( "WebServer " + d.name + " set isEnabled==" + str(d.isEnabled) );
                        break;

                self.wfile.write(json.dumps( { "success": True } ));
                return;

        elif (p[0] == "course"):
            if (p[1] == "get"):
                self.send_response(200, "OK");
                self.send_header("Content-type", "application/vnd.google-earth.kml+xml")
                self.end_headers()
                self.wfile.write( self.app.event.course.file );
                return;

        elif (p[0] == "settings"):
            if (p[1] == "get"):

                if "keys" in getParams:
                    keys = getParams["keys"].split(",");
                else:
                    self.send_response(200, "OK");
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing `keys` parameter"}));
                    return;

                query = "SELECT * FROM settings WHERE key IN ('" + "', '".join( keys ) + "')";
                q = self.db.do_query(query);

                settings = dict();
                while q.next():
                    settings[ q.value("key") ] = q.value("value");

                self.send_response(200, "OK");
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write( json.dumps( settings) );

        elif (p[0] == "summary"):
            if (p[1] == "get"):

                qDebug( self.path );
                self.send_response(200, "OK");
                self.send_header("Content-type", "application/json")
                self.end_headers()

                query = "SELECT * FROM stage1.apiCache WHERE key='gapTime/get'";
                q = self.db.do_query(query);

                gap = dict();
                while q.next():
                    if q.value("key") == "gapTime/get":
                        qDebug( q.value("value") );
                        gap = json.loads( q.value("value") );

                _out = [];
                for d in self.app.devices:
                    _device = dict();
                    _device["id"] = d.id;
                    _device["name"] = d.name;
                    _device["speed"] = numpy.round( d.speed*3.6, 1 );
                    _device["distance"] = numpy.round( d.distance / 1000, 1 );
                    _device["isEnabled"] = d.isEnabled;
                    _device["details"] = d.lastPosition.dict();
                    if d.addr in gap:
                        _device["gap"] = gap[ d.addr ];
                    else:
                        _device["gap"] = -1;

                    _out.append( _device );

                output = dict();
                output["devices"] = _out;

                groups = list();
                for g in self.app.groups:
                    groups.append( g.__dict__() );

                output["groups"] = groups;

                self.wfile.write(json.dumps(output));
                return;



        self.send_response(404, "API request does not exist");
