#!/usr/bin/python3

import sys

from xml.etree import ElementTree as ET
from xml.dom import minidom


class ConstructXML(object):
    def __init__(self):
        pass

    def _construct_xml(self, routes):
        root = ET.Element("schedule")
        for k, v in routes.items():
            route = ET.SubElement(root, "route")
            for row in v.values():
                row_elem = ET.SubElement(route, "row")
                if row["date"] is not None:
                    date = ET.SubElement(row_elem, "date")
                    date.text = row["date"]

                station = ET.SubElement(row_elem, "station")
                station.text = row["station"]

                if row["arrival"] is not None:
                    arrival = ET.SubElement(row_elem, "arrival")
                    arrival.text = row["arrival"]

                if row["departure"] is not None:
                    departure = ET.SubElement(row_elem, "departure")
                    departure.text = row["departure"]

                if row["vehicle"] is not None:
                    vehicle = ET.SubElement(row_elem, "vehicle")
                    vehicle.text = row["vehicle"]

                if row["delay"] is not None:
                    delay = ET.SubElement(row_elem, "delay")
                    delay.text = str(row["delay"])

        return root

    def _prettify(self, elem):
        rough_string = ET.tostring(elem, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def print_xml(self, routes):
        xml = self._construct_xml(routes)
        xml_str = self._prettify(xml)
        print(xml_str)
