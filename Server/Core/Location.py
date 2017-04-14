import datetime
import time

class Location:
    def __init__(self):
        self.longitude = 0;
        self.latitude = 0;
        self.altitude = 0;
        self.velocity = 0;
        self.vTheta = 0;
        self.vPhi = 0;
        self.direction = 0;
        self.time = 0;                                  #time recorded by device
        self.serverTime = int( time.time() * 1000)     #time recorded when time was recieved by server
        #times recorded in Epoch integer milliseconds

    def __str__(self):
        return ("N" if cmp( self.latitude, 0 ) else "S") + str(self.latitude) + "," \
            + ("E" if cmp(self.longitude, 0) else "W") + str(self.longitude) + "," \
            + str(self.altitude) + " - " \
            + str(self.velocity) + "(" \
            + str(self.vTheta) + "th" \
            + str(self.vPhi) + "ph) - " \
            + str(self.time);

    def __repr__(self):
        return self.__str__();



    def setPosition(self, long, lat, alt):
        self.longitude = float(long);
        self.latitude = float(lat);
        self.altitude = float(alt);

    def setVelocity(self, vel, vTheta, vPhi):
        self.velocity = float(vel);
        self.vTheta = float(vTheta);
        self.vPhi = float(vPhi);

    def setTime(self, t):
        self.time = int(t);