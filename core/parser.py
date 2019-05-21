#!/usr/bin/python3

import requests
import re

from bs4 import BeautifulSoup
from collections import defaultdict
from core.exceptions.exceptions import NotFound, InvalidInput

class Parser(object):
    """Scrapes cp.sk website to get current data"""

    def __init__(self, start, dest):
        self.start = start
        self.dest = dest

    def _get_data(self):
        url = "https://cp.hnonline.sk/vlakbusmhd/spojenie/"
        with requests.session() as s:
            s.headers["user-agent"] = "Mozilla/5.0"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            data = {
                "ctl00$cDM$cF$0t": self.start,
                "ctl00$cDM$cT$0t": self.dest,
                "ctl00$cDM$cSB$cmdSearch": "Hľadať",
                "IsDepTime": "true",
            }

            state = {
                tag["name"]: tag["value"] for tag in soup.select("input[name^=__]")
            }

            data.update(state)

            response = s.post(url, data=data)
            soup = BeautifulSoup(response.text, "html.parser")

            if soup.find("p", {"class": "errcont"}):
                raise InvalidInput("Invalid location entered")
            
            try:
                info = soup.find("b").find(text=True)
            except AttributeError:
                info = None
                
            if info == "Spojenie sa nenašlo.":
                raise NotFound("Route not found")

            return soup

    def get_routes(self):
        data = self._get_data()
        routes = defaultdict(dict)
        order = 1
        results = data.find_all("table", {"class": "results"})
        for result in results:
            route = defaultdict(dict)
            rows = result.find_all("tr", {"class": re.compile(r"^datarow")})
            row_count = 1
            for row in rows:
                processed_row = self._process_row(row)
                route[str(row_count)] = processed_row
                row_count += 1
            routes[str(order)] = route
            order += 1
        return routes

    def _process_row(self, row):
        elements = row.find_all("td")
        processed_row = dict()

        date = elements[1].find(text=True)
        station = elements[2].find(text=True)
        arrival = elements[3].find(text=True)
        departure = elements[4].find(text=True)
        vehicle = elements[6].find("a")

        if date == "\xa0":
            date = None

        if arrival == "\xa0":
            arrival = None

        if vehicle == "\xa0":
            vehicle = None

        if departure == "\xa0":
            departure = None

        try:
            vehicle_name = vehicle.find(text=True)
        except AttributeError:
            vehicle_name = None

        delay_data = row.find("div", {"class": "delaydiv"})
        delay_amount = None
        if delay_data is not None:
            delay = delay_data.find(text=True)
            delay_amount = [int(s) for s in delay.split() if s.isdigit()]
            if len(delay_amount) != 0:
                delay_amount = delay_amount.pop()
            else:
                delay_amount = None

        processed_row = {
            "date": date,
            "station": station,
            "arrival": arrival,
            "departure": departure,
            "vehicle": vehicle_name,
            "delay": delay_amount,
        }

        return processed_row
