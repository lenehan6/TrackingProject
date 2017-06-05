from PyQt5.QtCore import *
from PyQt5.QtSql import *

from AbstractObject import IODevice_AbstractObject, Type
from Server.Core.Location import Location
import xml.etree as XML
import time
import numpy


DEFAULT_INTERVAL = 500;  #milliseconds
EARTHS_RADIUS = 6378137;


class IODevice_SimulatorObject( IODevice_AbstractObject ):
    simulatorOutput = pyqtSignal('PyQt_PyObject');
    def __init__(self, id, contest, parent=None):
        super( IODevice_SimulatorObject, self ).__init__(contest, Type.Simulator, parent);
        self.avgSpeed = 40/3.6;              #Average speed of source
        self.avgLag = 200;                  #Average milliseconds different between fix time and recieve time
        self.avgPositionDeviation = 0.002   #Average deviation from the position in file
        self.loopAtEndOfFile = True         #Start file again when the file finishes
        self.pathCoords = [];               #Fill when simulation starts
        self.lastPosition = Location();
        self.addr = "SI:MU:LA:TO:R0:0" + str(id);
        self.delay = 0;

        ##for calculations
        self.counter = 0;
        self.course = 0;
        self.coords = list();
        self.wp_last = Location();
        self.wp_next = Location();

        self.e_lng = [0, 0, 0, 0, 0];
        self.e_lat = [0, 0, 0, 0, 0];
        self.e_alt = [0, 0, 0, 0, 0];

        self.thisPos = Location();

        self.timeOfLastCalc = time.time();

        self.workerThread = "";

        self.timer = QTimer( None );
        self.timer.setSingleShot( True );
        self.timer.setInterval( DEFAULT_INTERVAL );
        self.timer.timeout.connect( self.calculatePosition2 );


    def __del__(self):
        self.workerThread.quit();
        super(IODevice_SimulatorObject, self).__del__();

    def setThread(self, t):
        qDebug( "Thread set to " + str( t ) );
        self.workerThread = t;
        t.start();

        self.moveToThread( t );
        self.timer.moveToThread( t );


    def setSource(self, source):
        self.source = str(source);

    def setAvgSpeed(self, avgSpeed):
        self.avgSpeed = float(avgSpeed);

    def setAvgLag(self, avgLag):
        self.avgLag = int(avgLag);

    def setAvgPositionDeviation(self, deviation):
        self.avgPositionDeviation = float(deviation);

    def setDelay(self, delay):
        self.delay = delay;

    def getSaveData(self):
        saveData = self.getSaveData_AbstractObject();
        saveData["avgSpeed"] = self.avgSpeed;
        saveData["avgLag"] = self.avgLag;
        saveData["avgPositionDeviation"] = self.avgPositionDeviation;
        saveData["loopAtEndOfFile"] = self.loopAtEndOfFile;
        return saveData;

    @pyqtSlot(result=bool)
    def calculatePosition2(self):
        #qDebug( self.addr + " calculatePosition2()" );

        if ( self._quit ):
            qDebug( self.addr + " calculatePosition2() returned, self._quit == True")
            return False;

        now = time.time();
        interval = now - self.timeOfLastCalc;
        if ( interval > DEFAULT_INTERVAL*2/1000 ):
            qWarning( self.addr + " calculation interval ( " + str(int(interval*1000)) + "ms ) is very large" );

        self.timeOfLastCalc = now;

        self.lastPos = self.thisPos;

        self.distance += interval*self.avgSpeed;

        percentageComplete = (self.distance/self.contest.course.length);

        if ( self.loopAtEndOfFile and percentageComplete > 1 ):
            percentageComplete -= numpy.floor(percentageComplete);
        elif ( percentageComplete > 1 ):
            qDebug(self.addr + " calculatePosition2() returned, course complete")
            return False;

        self.thisPos = self.contest.course.pointAlongCourse( self.db, percentageComplete );
        self.thisPos.setVelocity( self.avgSpeed, numpy.arctan2( self.thisPos.latitude, self.thisPos.longitude ), 0 );
        self.thisPos.setDistance( int(self.distance) / 1000.0 );
        self.thisPos.setAddress( self.addr );
        self.thisPos.setTime( now*1000 );

        self.speed = self.avgSpeed;

        self.counter += 1;

        self.lastPosition = self.thisPos;
        self.simulatorOutput.emit( self.thisPos );
        #self.emit(SIGNAL("simulatorOutput(PyQt_PyObject)"), self.thisPos);
        if (self.counter == 1):
            qDebug( self.addr + "first position calculated" );

        ticks = time.time() - now;
        # if ( (ticks > DEFAULT_INTERVAL*2/1000) or (interval > DEFAULT_INTERVAL*2/1000) ):
        #     raise LookupError( self.addr + " calculatePosition2() took " + str( int(ticks*1000) ) + "ms to calculate" )
        #     qWarning( self.addr + " calculatePosition2() took " + str( int(ticks*1000) ) + "ms to calculate" );
        # else:
        #     qDebug( self.addr + " calculatePosition2() took " + str( int(ticks*1000) ) + "ms to calculate" );

        #run timer every DEFAULT INTERVAL, or immediately if interval is greater than DEFAULT_INTERVAL
        #qDebug( self.addr + " interval == " + str(interval) + ", timer reloaded with " + str( int( min( max(2*DEFAULT_INTERVAL - (interval*1000), 100),  DEFAULT_INTERVAL ) ) ) + "ms");
        self.timer.start( min( max(2*DEFAULT_INTERVAL - (interval*1000), 1),  DEFAULT_INTERVAL ) );
        self.timer.start();

        #qDebug(self.addr + "calculatePosition2() end of calc#" + str(self.counter) );
        return False;


    def start(self):
        if ( self.delay > 0 ):
            qDebug( self.addr + "waiting " + str(self.delay) + "ms to start" );

        QTimer.singleShot( self.delay, self.run );

    @pyqtSlot()
    def run(self):
        qDebug( "Simulator Running" );

        self.coords = list(self.contest.course.coords);
        self.timeOfLastCalc = time.time() - DEFAULT_INTERVAL/1000.0; #fake that last calc was one second ago.

        self.wp_last = self.coords.pop(0);
        self.wp_next = self.coords.pop(0);

        self.e_lng = [0, 0, 0, 0, 0];
        self.e_lat = [0, 0, 0, 0, 0];
        self.e_alt = [0, 0, 0, 0, 0];

        self.thisPos = Location();
        self.thisPos.setTime( time.time()*1000 );
        self.thisPos.setAddress( self.addr );
        self.calculatePosition2();





