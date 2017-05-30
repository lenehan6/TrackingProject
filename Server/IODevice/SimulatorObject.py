from PyQt4.QtCore import *
from PyQt4.QtSql import *

from AbstractObject import IODevice_AbstractObject, Type
from Server.Core.Location import Location
import xml.etree as XML
import time
import numpy


DEFAULT_INTERVAL = 0.5;  #seconds
EARTHS_RADIUS = 6378137;


class IODevice_SimulatorObject( IODevice_AbstractObject ):
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
        self.distance = 0;
        self.course = 0;
        self.coords = list();
        self.wp_last = Location();
        self.wp_next = Location();

        self.e_lng = [0, 0, 0, 0, 0];
        self.e_lat = [0, 0, 0, 0, 0];
        self.e_alt = [0, 0, 0, 0, 0];

        self.thisPos = Location();

        self.timeOfLastCalc = time.time();

        self.db = QSqlDatabase.addDatabase("QPSQL", "SIM"+str(id)+"_" + str(time.time()));
        self.db.setHostName("localhost");
        self.db.setPort(5432);
        self.db.setDatabaseName("events");



    def __del__(self):
        super(IODevice_SimulatorObject, self).__del__();



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

    def timerEvent(self, event):
        if ( ~self.calculatePosition2() ):
            self.killTimer( event.timerId() );


    def calculatePosition(self):
        if ( self._quit ):
            return;

        now = time.time();
        interval = now - self.timeOfLastCalc;
        self.timeOfLastCalc = now;

        self.lastPos = self.thisPos;

        dLong = self.wp_next.longitude - self.wp_last.longitude;
        dLat = self.wp_next.latitude - self.wp_last.latitude;
        dAlt = self.wp_next.altitude - self.wp_last.altitude;
        absD = (dLong ** 2 + dLat ** 2 + dAlt ** 2) ** (0.5);

        if (self.counter == 0):
            self.thisPos = self.wp_last;
        else:
            self.thisPos = Location();
            self.thisPos.setAddress(self.addr);
            self.thisPos.setTime(time.time() * 1000 + self.avgLag);
            theta = numpy.arctan2(dLong, dLat);
            phi = numpy.arctan2(dAlt, ((dLong ** 2 + dLat ** 2) ** (0.5)));
            self.thisPos.setVelocity(self.avgSpeed, theta, phi);

            # move "avgSpeed" from last wp to next
            long = self.lastPos.longitude + (dLong / absD) * (
            self.avgSpeed / (EARTHS_RADIUS * numpy.cos(numpy.pi * self.lastPos.longitude / 180))) * interval * 180 / numpy.pi
            lat = self.lastPos.latitude + (dLat / absD) * (self.avgSpeed / EARTHS_RADIUS) * interval * 180 / numpy.pi
            alt = self.lastPos.altitude + (dAlt / absD) * (self.avgSpeed / EARTHS_RADIUS) * interval * 180 / numpy.pi
            self.thisPos.setPosition(long, lat, alt);

            if (long > self.wp_next.longitude * (cmp(dLong, 0)) and
                        lat > self.wp_next.latitude * (cmp(dLat, 0))
                ):
                # if this coordinate has move passed the waypoint
                if (len(self.coords) == 0):
                    if self.loopAtEndOfFile:
                        # reload coords
                        self.coords = list(self.contest.course.coords);
                    else:
                        print "not looping to end of file, delete simulator at next chance"
                        self._quit = True;
                        self.deleteLater();
                        return;

                self.wp_last = self.wp_next;
                self.wp_next = self.coords.pop(0);
                # end if

                # track error from current line

        # end if
        self.counter += 1;

        self.lastPosition = self.thisPos;
        self.emit(SIGNAL("simulatorOutput(PyQt_PyObject)"), self.thisPos);
        if (self.counter == 1):
            print self.addr, "first position calculated";

    def calculatePosition2(self):
        print "calculatePosition2()"

        if ( self._quit ):
            return False;

        now = time.time();
        interval = now - self.timeOfLastCalc;
        self.timeOfLastCalc = now;

        self.lastPos = self.thisPos;

        self.distance += interval*self.avgSpeed;

        percentageComplete = self.distance/self.contest.course.length;
        if ( percentageComplete > 1 ):
            self.killTimer();
            return False;

        self.thisPos = self.contest.course.pointAlongCourse( self.db, percentageComplete );

        self.counter += 1;

        self.lastPosition = self.thisPos;
        self.emit(SIGNAL("simulatorOutput(PyQt_PyObject)"), self.thisPos);
        if (self.counter == 1):
            print self.addr, "first position calculated";

        return True;


    def start(self):
        if ( self.delay > 0 ):
            print self.addr, "waiting ", self.delay, "ms to start"

        QTimer.singleShot( self.delay, self, SLOT("run()") );

    @pyqtSlot()
    def run(self):
        print "Simulator Running";
        self.db.open();

        self.coords = list(self.contest.course.coords);

        self.wp_last = self.coords.pop(0);
        self.wp_next = self.coords.pop(0);

        self.e_lng = [0, 0, 0, 0, 0];
        self.e_lat = [0, 0, 0, 0, 0];
        self.e_alt = [0, 0, 0, 0, 0];

        self.thisPos = Location();
        self.thisPos.setTime( time.time()*1000 );
        self.thisPos.setAddress( self.addr );
        self.calculatePosition2();
        self.startTimer( DEFAULT_INTERVAL*1000 );




