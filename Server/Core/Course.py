from Location import Location

import xml.etree.ElementTree as ET
import re


class Course:
    def __init__(self, kmlFileLocation):
        with open(kmlFileLocation) as f:
            self.file = f.read();
            s = re.sub('<kml.+>', '<kml>', self.file);
            self.kml = ET.fromstringlist(s);
            s = str(self.kml.find(".//coordinates").text);

            self.coords = [];
            for line in s.split("\n"):
                line2 = line.split(",");
                if (len(line2) == 3):
                    wp = Location();
                    wp.setPosition(float(line2[0]), float(line2[1]), float(line2[2]));
                    self.coords.append(wp);

    def getClosestPointToCoordinate(self, (long, lat, alt), lastId=-1):
        # if lastId == -1, search whole file for closest point. Include lastId for faster fix.
        return (long, lat, alt);
