from Location import Location

import xml.etree.ElementTree as ET
import re

class Course:
    def __init__(self, kmlFileLocation):
        with open( kmlFileLocation ) as f:
            string = f.read();
            string = re.sub('<kml.+>', '<kml>', string);
            self.kml = ET.fromstringlist(string);
            string = str(self.kml.find(".//coordinates").text);

            self.coords = [];
            for line in string.split("\n"):
                line2 = line.split(",");
                if ( len(line2) == 3 ):
                    wp = Location();
                    wp.setPosition( float(line2[0]), float(line2[1]), float(line2[2]) );
                    self.coords.append( wp );


            print self.coords



    def getClosestPointToCoordinate(self, (long, lat, alt) , lastId = -1):
        #if lastId == -1, search whole file for closest point. Include lastId for faster fix.
        return (long, lat, alt);
