print "Running test_simulator"

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time
from Core.App import App
from Core.Event import Contest as Contest
from Core.Database import Database
from Core.Group import Group
from IODevice.SimulatorObject import IODevice_SimulatorObject
from WebUI.WebServer import WebServer
from ScoringEngine.GapTimeEngine import ScoringEngine_GapTimeEngine

import webbrowser
import os, sys

log_mutex = QMutex();
def qt_message_handler(mode, message):
    QMutexLocker( log_mutex );

    # if mode != QtCore.QtInfoMsg:
    #     ('line: %d, func: %s(), file: %s' % (
    #       context.line, context.function, context.file))

    style = '0';
    mode = '';
    if mode == QtDebugMsg:
        mode = ''
    elif mode == QtWarningMsg:
        mode = 'WARNING'
        style = '0;31;40'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
        style = '0;30;41'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
        style = '0;30;41'
    else:
        mode = ''

    print '\x1b[%sm %s %s: (%s) %s \x1b[0m' % (style, int(time.time()*1000), mode, QThread.currentThread(), message);


qapp = QCoreApplication(sys.argv)
qDebug( "QCoreApplication started" )

# qInstallMessageHandler(qt_message_handler);
# qDebug( "Message handler installed" )

##create objects before starting event loop
app = App();

db = Database();
app.setDatabase( db );

contest = Contest();
contest.setDatabase( db );
contest.setCourse( "/Users/jameslenehan/Git/TrackingProject/Testing/Untitled map.kml" );

app.setContest( contest );
app.deleteEventData();


i = 1;
device = IODevice_SimulatorObject( i, contest );
device.setDeviceName( "simulator1" );
device.setAvgSpeed( 50/3.6 );
device.setDatabase( db );
t = QThread();
device.setThread( t );
device.start();
app.addDevice( device );
i += 1;

device2 = IODevice_SimulatorObject( i, contest );
device2.setDeviceName( "simulator2" );
device2.setDelay( 1000 );
device2.setAvgSpeed( 55/3.6 );
device2.setDatabase( db );
t2 = QThread();
device2.setThread( t2 );
device2.start();
app.addDevice( device2 );
i += 1;

device3 = IODevice_SimulatorObject( i, contest );
device3.setDeviceName( "simulator3" );
device3.setDelay( 1000 );
device3.setAvgSpeed( 45/3.6 );
device3.setDatabase( db );
t3 = QThread();
device3.setThread( t3 );
device3.start();
app.addDevice( device3 );
i += 1;


engine = ScoringEngine_GapTimeEngine( contest );
engine.setDatabase( db );
app.setScoringEngine( engine );
engine.start();

app.dbLocationsUpdated.connect( engine.calculateCurrentGap );

group1 = Group( app );
group1.setName( "Peleton" );
group1.setDevice( device3 );
app.addGroup( group1 );

group2 = Group( app );
group2.setName( "Leader" );
group2.setDevice( device2 );
app.addGroup( group2 );


os.chdir("WebUI");
www = WebServer( app );
www.setDatabase( db );
www.start();

app.setWebServer( www );

webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) + "/api/locations/get");
webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) + "/api/summary/get");
webbrowser.open( "http://" + www.HOST + ":" + str(www.PORT) );

##create eventloop and wait
qDebug( "Enter event loop" );
sys.exit(qapp.exec_())

print "Application quit";
www.quit();
device.quit();
device2.quit();




