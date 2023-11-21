"""
A rikishi represents an individual wrestler that is part of a beya and therefore the association as a whole
"""
from utils.fetch import fetchRikishi
from utils.exceptions import RikishiNotFoundError
import utils.constants as constants

TAGS = ['\t', '\r', '<tr>', "</tr>", "<td>", "</td>", "<table>", "</table>"]

ATTRIBUTES = ["higestRank", "realName", "birthDate", "shusshin", "heya", ""]

class Rikishi:
    """
    Create a Rikishi based on either the stats itself or on the year and month
    If year and month given get the rikishi that fought with that shikona in that tournament
    Otherwise, simply take the stats and create that object
    URL takes in the shikona, year, and month as URL parameters
    Ex: Takakeisho = https://sumodb.sumogames.de/Rikishi.aspx?shikona=takakeisho&b=202301
    """
    def __init__(self, shikona, **kwargs):
        self.shikona = shikona

        if "year" and "month" in kwargs:
            year, month = kwargs['year'], kwargs['month']
            rikishiInfo = self._retrieveRikishi(shikona, year, month)
            print(rikishiInfo)
           
    
    def getShikona(self):
        return self.shikona
               
    def _retrieveRikishi(self, shikona: str, year: int, month: int):
        rikishi = fetchRikishi(shikona, year, month)
        if "404" in rikishi or "Highest Rank" not in rikishi:
            raise RikishiNotFoundError(shikona, year, month)
        rikishi = rikishi.split("<td class=\"layoutright\">")[1].split("<br />")[0].split("\n")
        for i in range(0, len(rikishi)):
            for tag in TAGS:
                rikishi[i] = rikishi[i].replace(tag, "").strip()
        rikishi = [i for i in rikishi if i.startswith("<td class=\"cat\"") ]
        rikishiInfo = {}
        for i in rikishi:
            attributes = i.replace("<td class=\"cat\">", "").replace("&nbsp", "").lstrip(";").strip().split("<td class=\"val\">")
            if len(attributes) == 2:
                rikishiInfo[attributes[0]] = attributes[1]
        
        # Clean the dictionary into necessary attributes
        # Height and Weight
        hwSplit = rikishiInfo["Height and Weight"].split()
        rikishiInfo["height"], rikishiInfo["weight"] = hwSplit[0], hwSplit[2]
        del rikishiInfo["Height and Weight"]

        # Split beyas into a list
        rikishiInfo["Heya"] = rikishiInfo["Heya"].split(" - ")

        # Split shikonas into a list
        rikishiInfo["Shikona"] = rikishiInfo["Shikona"].split(" - ")

        # Compile divisional records into a dictionary of dictionaries
        rikishiRecords = {}
        for division in constants.DIVISIONS:
            rikishiRecords[division] = rikishiInfo[f"In {division}"]


        

        return rikishiRecords
    
    