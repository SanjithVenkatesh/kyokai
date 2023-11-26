"""
This module contains all logic for creating a Rikishi object

A Rikishi is an individual wrestler that is a part of a Beya (stable) and ultimately part of the Kyokai.
"""
import copy, re
from typing import Dict
from utils.fetch import fetchRikishi
from utils.exceptions import RikishiNotFoundError
import utils.constants as constants
from utils.birthDate import birthDate

TAGS = ["\t", "\r", "<tr>", "</tr>", "<td>", "</td>", "<table>", "</table>"]

SPECIAL_PRIZES = {"shukun-sho": 0, "kanto-sho": 0, "gino-sho": 0, "kinboshi": 0}
DIVISION_INFO = {"wins": 0, "loses": 0, "absences": 0, "yusho": 0, "jun-yusho": 0}

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
            year, month = kwargs["year"], kwargs["month"]
            rikishiInfo = self._retrieveRikishi(shikona, year, month)
            print(rikishiInfo)
            for k, v in rikishiInfo.items():
                setattr

    def getShikona(self):
        return self.shikona

    def _retrieveRikishi(self, shikona: str, year: int, month: int):
        rikishi = fetchRikishi(shikona, year, month)
        if "404" in rikishi or "Highest Rank" not in rikishi:
            raise RikishiNotFoundError(shikona, year, month)
        rikishi = (
            rikishi.split('<td class="layoutright">')[1].split("<br />")[0].split("\n")
        )
        for i in range(0, len(rikishi)):
            for tag in TAGS:
                rikishi[i] = rikishi[i].replace(tag, "").strip()
        rikishi = [i for i in rikishi if i.startswith('<td class="cat"')]
        rikishiInfo = {}
        for i in rikishi:
            attributes = (
                i.replace('<td class="cat">', "")
                .replace("&nbsp", "")
                .lstrip(";")
                .strip()
                .split('<td class="val">')
            )
            if len(attributes) == 2:
                rikishiInfo[attributes[0]] = attributes[1]
        
        # Re-format the highest rank, real name, shusshin, hatsu dohyo
        rikishiInfo['highestRank'] = rikishiInfo['Highest Rank']
        del rikishiInfo['Highest Rank']
        rikishiInfo['realName'] = rikishiInfo['Real Name'].lower().capitalize()
        del rikishiInfo['Real Name']
        # TODO: create a util object to represent the shusshin
        rikishiInfo['shusshin'] = rikishiInfo['Shusshin']
        # TODO: modify the birthDate class to be a general Date class
        rikishiInfo['hatsuDohyo'] = rikishiInfo['Hatsu Dohyo']
        del rikishiInfo['Hatsu Dohyo']
        del rikishiInfo['Shusshin']

        # Clean the dictionary into necessary attributes
        # Height and Weight
        hwSplit = rikishiInfo["Height and Weight"].split()
        rikishiInfo["height"], rikishiInfo["weight"] = hwSplit[0], hwSplit[2]
        del rikishiInfo["Height and Weight"]

        # Split beyas into a list
        rikishiInfo["heya"] = rikishiInfo["Heya"].split(" - ")
        del rikishiInfo["Heya"]

        # Split shikonas into a list
        rikishiInfo["shikona"] = rikishiInfo["Shikona"].split(" - ")
        del rikishiInfo["Shikona"]

        # Compile divisional records into a dictionary of dictionaries
        rikishiRecords = {}
        for division in constants.DIVISIONS:
            try:
                rikishiRecords[division] = self._parseRecord(
                    division, rikishiInfo[f"In {division}"]
                )
                del rikishiInfo[f"In {division}"]
            except:
                rikishiRecords[division] = None

        # Get record for ranks within Makuuchi
        withinMakuuchi = {}
        for rank in constants.MAKUUCHI_RANKS:
            try:
                withinMakuuchi[rank] = self._parseRecord(
                    division, rikishiInfo[f"As {rank}"]
                )
                del rikishiInfo[f"As {rank}"]
            except:
                withinMakuuchi[rank] = None

        rikishiRecords["Makuuchi"]["withinMakuuchi"] = withinMakuuchi
        rikishiInfo["records"] = rikishiRecords

        # Handle total career record
        careerPattern = r'(\d+)'
        careerNumbers = re.findall(careerPattern, rikishiInfo['Career Record'])
        careerNumbers = [int(number) for number in careerNumbers]
        careerRecord = {"wins": careerNumbers[0], "loses": careerNumbers[1], "totalBouts": careerNumbers[2], "bashos": careerNumbers[3]}
        rikishiInfo["records"]["total"] = careerRecord
        del rikishiInfo['Career Record']

        # Handle Mae-zumo and Banzuke-gai stats
        getDigit = r'(\d+)'
        rikishiInfo['maezumo'] = int(re.search(getDigit, rikishiInfo['In Mae-zumo']).group(1))
        rikishiInfo['banzukegai'] = int(re.search(getDigit, rikishiInfo['In Banzuke-gai']).group(1)) if 'In Banzuke-gai' in rikishiInfo else 0
        del rikishiInfo['In Mae-zumo']
        if 'In Banzuke-gai' in rikishiInfo:
            del rikishiInfo['In Banzuke-gai']

        rikishiInfo['birthDate'] = birthDate(rikishiInfo['Birth Date'])
        del rikishiInfo['Birth Date']

        self.retired = False
        # Handle retired Rikishi
        if "Intai" in rikishiInfo:
            rikishiInfo['intai'] = rikishiInfo['Intai']
            self.retired = True

        return rikishiInfo

    def _parseRecord(self, division: str, recordString: str) -> Dict[str, int]:
        """
        Given a string like the following:
        '77-54-4/130 (9 basho), 1 Jun-Yusho, 2 Shukun-Sho, 1 Kanto-Sho, 3 Kinboshi'
        We should parse this into the following dictionary:
        {'wins': 77, 'loses': 54, 'absences': 4, 'yusho': 0, 'jun-yusho': 1,
        'special': {'shukun-sho': 2, 'kanto-sho': 1, 'kinboshi': 3, 'gino-sho': 0}}
        """
        stats = {}

        divisionInfoSplit = recordString.split(",")
        stats = copy.deepcopy(DIVISION_INFO)
        if division == "Makuuchi":
            stats["special"] = copy.deepcopy(SPECIAL_PRIZES)

        # First get the overall wins, loses, and absences for the division, it will be the first item of the split
        wlaPattern = r"\b(\d+)\b"
        wlaList = [int(n) for n in re.findall(wlaPattern, divisionInfoSplit[0])]
        stats["wins"], stats["loses"] = wlaList[0], wlaList[1]
        stats["absences"] = wlaList[2] if len(wlaList) > 4 else 0
        stats["bouts"] = stats["wins"] + stats["loses"] + stats["absences"]

        # Now we will get the special awards
        # Start with yushos and jun-yushos since that is relevant for all divisions
        for specialAward in divisionInfoSplit[1:]:
            specialAward = specialAward.strip().lower()
            yushos = ["yusho", "jun-yusho"]
            for y in yushos:
                if y in specialAward:
                    stats[y] = int(specialAward.split()[0])

            # Now look at the rest of the special awards if the division is Makuuchi as those awards are only relevant to that division
            if division == "Makuuchi":
                for saToLookFor in list(SPECIAL_PRIZES.keys()):
                    if saToLookFor in specialAward:
                        stats["special"][saToLookFor] = int(specialAward.split()[0])

        return stats
