print "Running test_simulator"

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time
from Core.App import App
from Core.Event import Contest as Contest
from Core.Database import Database
from IODevice.SimulatorObject import IODevice_SimulatorObject
from WebUI.WebServer import WebServer

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
device2.setDelay( 5.7 * 1000 );
device2.setAvgSpeed( 45/3.6 );
device2.setDatabase( db );
t2 = QThread();
device2.setThread( t2 );
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
qDebug( "Enter event loop" );
sys.exit(qapp.exec_())

print "Application quit";
www.quit();
device.quit();
device2.quit();




