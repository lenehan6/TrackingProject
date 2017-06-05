from PyQt5.QtCore import *
from PyQt5.QtSql import *
from Core.Location import Location
from AbstractObject import ScoringEngine_AbstractObject, Type
import json
from enum import *

from scipy.signal import butter, lfilter
from numpy.fft import fft, ifft

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


TIME_WINDOW         = 10    #consider last 60 seconds of data for gap time
SAMPLING_FREQUENCY  = 5     #using a sampling frequency of 5 seconds

class ScoringEngine_GapTimeEngine( ScoringEngine_AbstractObject ):
    def __init__(self, contest, parent=None):
        super( ScoringEngine_GapTimeEngine, self ).__init__(Type.GapTime, contest, parent);
        #manually update every 5 seconds
        self.updateInterval = 5000;
        self.gapTimes = dict();
        self.gap = dict();
        #end __init__

    def timerEvent(self, event):
        return self.calculateCurrentGap();


    def currentLocation(self):
        locs = list();
        leader = "";

        query = "SELECT t.id, t.mac, t.time, t.distance, t.speed, t.longitude, t.latitude, t.altitude FROM (SELECT mac, MAX(distance) AS distance FROM stage1.gpsLocations GROUP BY mac) last JOIN stage1.gpsLocations t ON last.mac=t.mac AND last.distance=t.distance ORDER BY t.distance DESC";
        q = self.db.do_query( query );
        q.exec_(query);
        while ( q.next() ):
            loc = Location();
            addr = q.value("mac");
            loc.setAddress( addr );
            loc.setPosition( q.value("longitude"),
                             q.value("latitude"),
                             q.value("altitude")
                             );
            loc.setTime( q.value("time") );
            loc.setDistance( q.value("distance") );
            locs.append( loc );
            if addr == self.contest.leader:
                leader = loc;


        if len( locs ) == 0:
            return None, None;

        if ( leader == "" ):
            leader = locs[0];

        return leader, locs;

    @pyqtSlot()
    def calculateCurrentGap(self):

        leader, locations = self.currentLocation();

        if ( leader == None and locations == None ):
            qDebug( "No locations returned from currentLocation()" );
            return;

        gap = dict();
        for l in locations:

            if l.addr not in self.gapTimes:
                self.gapTimes[ l.addr ] = dict();

            if ( l == leader ):
                self.gapTimes[ l.addr ][ l.time ] = 0;
                self.gap[l.addr] = 0;
                #leader will not return any results as no one is at that distance yet
                continue;

            query = "(SELECT t.* FROM ( SELECT mac, MAX(distance) AS distance FROM stage1.gpsLocations WHERE distance<=" + str( l.distance ) + " AND mac='" + leader.addr + "' GROUP BY mac ) near JOIN stage1.gpsLocations t ON t.distance=near.distance AND t.mac=near.mac UNION SELECT t.* FROM ( SELECT mac, MIN(distance) AS distance FROM stage1.gpsLocations WHERE distance>" + str( l.distance ) + " AND mac='" + leader.addr + "' GROUP BY mac ) near JOIN stage1.gpsLocations t ON t.distance=near.distance AND t.mac=near.mac) ORDER BY mac, distance;"
            #qDebug( query );
            q = self.db.do_query( query );

            i = 0;
            x = dict(); #distance along course in metres
            t = dict(); #timestamp of position in seconds
            while q.next():
                x[ i ] = q.value("distance")*1000;
                t[ i ] = q.value("time")*1.0/1000;
                i += 1;


            #qDebug( "x0==" + str(l.distance*1000) + ", x==" + x.__repr__() + ", t==" + t.__repr__() );
            if ( i != 2 ):
                qWarning( "query returned unexpected amount of results" );
                continue;

            if ( x[0] == x[1] ):
                qWarning("query returned identical positons");
                continue;

            #gap[l.addr] = (l.time / 1000.0) - t[0];
            gap = max( (l.time/1000.0) - ( t[0] + ( t[1] - t[0] )*( l.distance*1000 - x[0] )/( x[1] - x[0] ) ), 0 );

            self.gapTimes[ l.addr ][ l.time ] = gap;
            self.gap[ l.addr ] = gap;


        #self.smoothResult();
        ## do further smoothing of calculation here
        ## 1. smooth over frequency domain, for variations in gap time, (butterworth filter with f_c=1/40)
        ## 2. use a weighting function to give more influence on more recent times. (triangle window, accepting over last minute)

        self.resultReady.emit( self.gap );
        self.writeResultToCache();

        return

    def writeResultToCache(self):
        j = json.dumps( self.gap );
        query = "INSERT INTO stage1.apiCache (key, value) VALUES ('gapTime/get', '" + j + "') ON CONFLICT (key) DO UPDATE SET value='" + j + "'";
        q = self.db.do_query( query );
        if q.lastError().type() != QSqlError.NoError:
            qDebug( q.lastError().text() + " (" + q.lastQuery() + ")" );
        return;

    # def smoothResult(self):
    #
    #     for addr in self.gapTimes:
    #         addr_dict = self.gapTimes[ addr ];
    #
    #         gap_raw     = addr_dict.values();
    #         time_raw    = addr_dict.keys();
    #
    #         if (len(time_raw) == 1):
    #             return;
    #
    #         qDebug(time_raw.__repr__());
    #
    #         gap = list();
    #         time = list();
    #         #time_spacing = list();
    #         max_t   = time_raw[-1];
    #         t       = time_raw[-1];
    #         temp    = dict();
    #         while ( t > max_t - 1000*TIME_WINDOW ):
    #             #diff = time_raw[-1] - time_raw[-2];
    #             #time_spacing.append( diff );
    #             g_last = gap_raw.pop();
    #             t_last = time_raw.pop();
    #             gap.append( g_last );
    #             time.append( t_last );
    #             temp[t_last] = g_last;
    #
    #             if ( len( time_raw )==0 ):
    #                 break;
    #             t = time_raw[-1];
    #
    #         self.gapTimes[addr] = temp;
    #
    #         #T_avg = sum(time_spacing)/len(time_spacing);
    #         T_avg = 0.5;
    #         data = [ gap, time ];
    #
    #         FFT = fft( data );
    #         qDebug(FFT.__repr__());
    #         filtered = ifft( butter_bandpass_filter( FFT, 0, 40/T_avg, 1/T_avg, 4 ) )
    #         qDebug( filtered.__repr__() );









