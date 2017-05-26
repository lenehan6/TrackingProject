from PyQt4.QtCore import *

from AbstractObject import IODevice_AbstractObject, Type
from Server.Core.Location import Location
import xml.etree as XML
import time
import numpy


DEFAULT_INTERVAL = 0.5;
EARTHS_RADIUS = 6378137;


class IODevice_SimulatorObject( IODevice_AbstractObject ):
    def __init__(self, contest, parent=None):
        super( IODevice_SimulatorObject, self ).__init__(contest, Type.Simulator, parent);
        self.avgSpeed = 40/3.6;              #Average speed of source
        self.avgLag = 200;                  #Average milliseconds different between fix time and recieve time
        self.avgPositionDeviation = 0.002   #Average deviation from the position in file
        self.loopAtEndOfFile = True         #Start file again when the file finishes
        self.pathCoords = [];               #Fill when simulation starts
        self.lastPosition = '';

    def setSource(self, source):
        self.source = str(source);

    def setAvgSpeed(self, avgSpeed):
        self.avgSpeed = float(avgSpeed);

    def setAvgLag(self, avgLag):
        self.avgLag = int(avgLag);

    def setAvgPositionDeviation(self, deviation):
        self.avgPositionDeviation = float(deviation);

    def getSaveData(self):
        saveData = self.getSaveData_AbstractObject();
        saveData["avgSpeed"] = self.avgSpeed;
        saveData["avgLag"] = self.avgLag;
        saveData["avgPositionDeviation"] = self.avgPositionDeviation;
        saveData["loopAtEndOfFile"] = self.loopAtEndOfFile;
        return saveData;

    def run(self):
        print "Simulator Running";
        coords = list(self.contest.course.coords);

        wp_last = coords.pop(0);
        wp_next = coords.pop(0);

        e_lng = [0, 0, 0, 0, 0];
        e_lat = [0, 0, 0, 0, 0];
        e_alt = [0, 0, 0, 0, 0];
        i = 0;

        thisPos = Location();
        thisPos.setTime( time.time()*1000 );
        thisPos.setAddress( self.addr );
        interval = DEFAULT_INTERVAL;
        while not self._quit:
            lastPos = thisPos;

            dLong = wp_next.longitude - wp_last.longitude;
            dLat = wp_next.latitude - wp_last.latitude;
            dAlt = wp_next.altitude - wp_last.altitude;
            absD = (dLong ** 2 + dLat ** 2 + dAlt ** 2) ** (0.5);

            if ( i == 0 ):
                thisPos = wp_last;
            else:
                thisPos = Location();
                thisPos.setAddress(self.addr);
                thisPos.setTime( time.time() * 1000 + self.avgLag);
                theta = numpy.arctan2(dLong, dLat);
                phi = numpy.arctan2( dAlt, ((dLong ** 2 + dLat ** 2) ** (0.5)) );
                thisPos.setVelocity(self.avgSpeed, theta, phi);

                #move "avgSpeed" from last wp to next
                long = lastPos.longitude + (dLong/absD)*(self.avgSpeed / (EARTHS_RADIUS * numpy.cos(numpy.pi * lastPos.longitude / 180))) * interval * 180 / numpy.pi
                lat = lastPos.latitude + (dLat/absD) * (self.avgSpeed / EARTHS_RADIUS) * interval * 180 / numpy.pi
                alt = lastPos.altitude + (dAlt/absD) * (self.avgSpeed / EARTHS_RADIUS) * interval * 180 / numpy.pi
                thisPos.setPosition(long, lat, alt);

                if ( long > wp_next.longitude*( cmp(dLong, 0) ) and
                     lat > wp_next.latitude*( cmp( dLat, 0 ) )
                     ):
                    #if this coordinate has move passed the waypoint
                    if ( len(coords) == 0 ):
                        if self.loopAtEndOfFile:
                            #reload coords
                            coords = list(self.contest.course.coords);
                        else:
                            self.quit = True;
                            continue;

                    wp_last = wp_next;
                    wp_next = coords.pop(0);
                #end if

                #track error from current line

            #end if
            i += 1;

            self.lastPosition = thisPos;
            self.emit( SIGNAL("simulatorOutput(PyQt_PyObject)"), thisPos );
            time.sleep( interval );
        #end while


        print "end of simulation!";


