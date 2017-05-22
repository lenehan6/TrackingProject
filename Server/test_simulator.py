import time
from Core.App import App
from Core.Event import Event as Event
from IODevice.SimulatorObject import IODevice_SimulatorObject
from WebUI.WebServer import WebServer

import webbrowser
import os, sys

app = App();

event = Event();
event.setCourse( "/Users/jameslenehan/Git/TrackingProject/Testing/Untitled map.kml" );

app.setEvent( event );

device = IODevice_SimulatorObject( event );
device.setDeviceName( "simulator1" );
device.start();

app.addDevice( device );

os.chdir("WebUI");
www = WebServer( app );
www.start();

app.setWebServer( www );

webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) + "/api/locations/get");
webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT));


while True:
    try:
        print "Main thread running"
        time.sleep(1000);
    finally:
        www.quit();
        device.quit();
        break;




