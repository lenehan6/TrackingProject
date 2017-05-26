from PyQt4.QtCore import *
from PyQt4.QtGui import *

import time
from Core.App import App
from Core.Event import Contest as Contest
from IODevice.SimulatorObject import IODevice_SimulatorObject
from WebUI.WebServer import WebServer

import webbrowser
import os, sys

qapp = QApplication(sys.argv)

##create objects before starting event loop

app = App();

contest = Contest();
contest.setCourse( "/Users/jameslenehan/Git/TrackingProject/Testing/Untitled map.kml" );

app.setContest( contest );

device = IODevice_SimulatorObject( contest );
device.setDeviceName( "simulator1" );
device.start();

app.addDevice( device );

os.chdir("WebUI");
www = WebServer( app );
www.start();

app.setWebServer( www );

webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) + "/api/locations/get");
webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) );

##create eventloop and wait

sys.exit(qapp.exec_())

print "Application quit";
www.quit();
device.quit();




