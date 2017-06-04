from Location import Location
import time

from PyQt5.QtCore import *
from PyQt5.QtSql import *

import xml.etree.ElementTree as ET
import re


class Course(QObject):
    def __init__(self, kmlFileLocation, db):
        qDebug( "new Course() object (" + kmlFileLocation + ")" );
        QObject.__init__(self, None);
        self.length = 0;
        self.db = db;

        query = "DELETE FROM stage1.course";
        q = self.db.do_query( query );

        query = "DELETE FROM stage1.course2";
        q = self.db.do_query(query);

        with open(kmlFileLocation) as f:
            self.file = f.read();
            s = re.sub('<kml.+>', '<kml>', self.file);
            self.kml = ET.fromstringlist(s);
            s = str(self.kml.find(".//coordinates").text);

            values = [];

            self.coords = [];
            for line in s.split("\n"):
                line2 = line.split(",");
                if (len(line2) == 3):
                    wp = Location();
                    wp.setPosition(float(line2[0]), float(line2[1]), float(line2[2]));
                    self.coords.append(wp);
                    #values.append( "'POINT("+str(float(line2[0]))+" "+line2[1]+" "+line2[2]+")'::geometry" );
                    values.append( str(float(line2[0]))+" "+line2[1]+" "+line2[2] );

            #query = "INSERT INTO stage1.course (pos) VALUES (" + '), ('.join(values) + ")";
            query = "INSERT INTO stage1.course2 (sector, line) VALUES ( 1, 'LINESTRING(" + ', '.join(values) + ")'::geography )";
            q = self.db.do_query(query);

            tick = time.time();
            query = "SELECT sector, ST_Length(line) as line_distance FROM stage1.course2";
            q = self.db.do_query(query);

            if ( q.lastError().type() == QSqlError.NoError ):
                output = "Sector distances\rSector\t| Distance (km) \n------------------------------------ \n"

                sum = 0;
                while q.next():
                    dist = q.value("line_distance");
                    sum += dist;
                    output += ( str(q.value("sector")) + "\t\t| " + str(dist/1000) ) + "\n";

                qDebug( output +
                        "------------------------------------\n" + \
                        "TOTAL\t| " + str( sum/1000 ) + "\n" + \
                        "(Query took " + str( time.time() - tick ) + "s)" )

                self.length = sum;
        qDebug( "Course() initalised" );





    def pointAlongCourse(self, dbConn, percentage):

        qDebug( "Course.pointAlongCourse()" );
        tick = time.time();
        if ( percentage > 1.0 ):
            qDebug( "percentage (", percentage, ") is greater than 1, returning" )
            return Location();

        # if ~(dbConn.isOpen()):
        #     dbConn.open();
        #     print "db (", dbConn.connectionName(), ") is not open, attempted to open"



        query = "SELECT ST_AsText(ST_LineInterpolatePoint(line::geometry, " + str(percentage) + ")) as position FROM stage1.course2";
        q = self.db.do_query( query );

        point = Location();

        if ( q.lastError().type() == QSqlError.NoError ):
            while q.next():
                result = q.value("position");
                #print result;
                r = re.compile('[POINT Z ()]+')
                #print "regexp returns", r.split( result );
                coords = r.split( result );
                point.setPosition( coords[1], coords[2], coords[3] );
                break; #only looking for 1 result

        tock = time.time() - tick;
        if ( tock > 0.2 ):
            qWarning( "pointAlongCourse() took ", time.time() - tick, "seconds to return" );

        return point;
