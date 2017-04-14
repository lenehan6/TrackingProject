import time
from Core.Event import Event as Event
from IODevice.SimulatorObject import IODevice_SimulatorObject

event = Event();
event.setCourse( "/Users/jameslenehan/Git/TrackingProject/Testing/Untitled map.kml" );

device = IODevice_SimulatorObject( event );

device.start();

while True:
    print "Main thread running"
    time.sleep(100);



