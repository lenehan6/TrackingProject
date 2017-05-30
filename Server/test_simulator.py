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
app.deleteEventData();


i = 1;
device = IODevice_SimulatorObject( i, contest );
device.setDeviceName( "simulator1" );
device.setAvgSpeed( 40/3.6 );
device.start();
app.addDevice( device );
i += 1;

device2 = IODevice_SimulatorObject( i, contest );
device2.setDeviceName( "simulator2" );
device2.setDelay( 5 * 1000 );
device.setAvgSpeed( 35/3.6 );
device2.start();
app.addDevice( device2 );
i += 1;


os.chdir("WebUI");
www = WebServer( app );
www.start();

app.setWebServer( www );

webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) + "/api/locations/get");
webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) );

##create eventloop and wait
print "Enter event loop";
sys.exit(qapp.exec_())

print "Application quit";
www.quit();
device.quit();
device2.quit();




