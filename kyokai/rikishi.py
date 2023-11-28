"""
This module contains all logic for creating a Rikishi object

A Rikishi is an individual wrestler that is a part of a Beya (stable) and ultimately part of the Kyokai.
"""
import copy, re
from typing import Dict
from kyokai.utils.fetch import fetchRikishi
from kyokai.utils.exceptions import RikishiNotFoundError
import kyokai.utils.constants as constants
from kyokai.utils.date import Debut, BirthDate

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

    def __init__(self, shikona, *args, **kwargs):
        self.shikona = shikona

        if "year" and "month" in kwargs:
            year, month = kwargs["year"], kwargs["month"]
            self._retrieveRikishi(shikona, year, month)
        elif len(args) == 2:
            if type(args[0]) is not int or type(args[1]) is not int:
                raise Exception("Invalid argument types to create Rikishi!")
            self._retrieveRikishi(shikona, args[0], args[1])

    def getCurrentShikona(self):
        if type(self.shikona) == list:
            return self.shikona[-1]
        else:
            return self.shikona
    
    def getCurrentHeya(self):
        if type(self.heya) == list:
            return self.heya[-1]
        else:
            return self.heya
    
    def getDebut(self):
        return self.debut
    
    def getCareerWins(self):
        return self.records["total"]["wins"]

    def getCareerLoses(self):
        return self.records["total"]["loses"]
    
    # Division here has to be a division name, not a number
    def getDivisionWins(self, division: str):
        return self.records[division.lower().capitalize()]['wins']
    
    def getDivisionLoses(self, division: str):
        return self.records[division.lower().capitalize()]['loses']

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
        self.highestRank = rikishiInfo['Highest Rank']
        self.realName = rikishiInfo['Real Name'].lower().capitalize()
        # TODO: create a util object to represent the shusshin
        self.shusshin = rikishiInfo['Shusshin']
        
        self.debut = Debut(rikishiInfo['Hatsu Dohyo'])

        # Clean the dictionary into necessary attributes
        # Height and Weight
        hwSplit = rikishiInfo["Height and Weight"].split()
        # rikishiInfo["height"], rikishiInfo["weight"] = hwSplit[0], hwSplit[2]
        self.heigh, self.weight = hwSplit[0], hwSplit[2]

        # Split beyas into a list
        self.heya = rikishiInfo["Heya"].split(" - ")

        # Split shikonas into a list
        self.shikona = rikishiInfo["Shikona"].split(" - ")
        self.records = self._getRecords(rikishiInfo)

        # Handle Mae-zumo and Banzuke-gai stats
        getDigit = r'(\d+)'
        self.maezumo = int(re.search(getDigit, rikishiInfo['In Mae-zumo']).group(1))
        self.banzukegai = int(re.search(getDigit, rikishiInfo['In Banzuke-gai']).group(1)) if 'In Banzuke-gai' in rikishiInfo else 0

        self.birthDate = BirthDate(rikishiInfo['Birth Date'])

        # Handle retired Rikishi
        self.intai, self.retired = None, False
        if "Intai" in rikishiInfo:
            self.intai, self.retired = rikishiInfo['Intai'], True
    
    def _getRecords(self, rikishiInfo):
        # Compile divisional records into a dictionary of dictionaries
        rikishiRecords = {}
        for division in constants.DIVISIONS:
            try:
                rikishiRecords[division] = self._parseRecord(
                    division, rikishiInfo[f"In {division}"]
                )
            except:
                rikishiRecords[division] = None

        # Get record for ranks within Makuuchi
        withinMakuuchi = {}
        for rank in constants.MAKUUCHI_RANKS:
            try:
                withinMakuuchi[rank] = self._parseRecord(
                    division, rikishiInfo[f"As {rank}"]
                )
            except:
                withinMakuuchi[rank] = None

        rikishiRecords["Makuuchi"]["withinMakuuchi"] = withinMakuuchi

        # Handle total career record
        careerPattern = r'(\d+)'
        careerNumbers = re.findall(careerPattern, rikishiInfo['Career Record'])
        careerNumbers = [int(number) for number in careerNumbers]
        careerRecord = {"wins": careerNumbers[0], "loses": careerNumbers[1], "totalBouts": careerNumbers[2], "bashos": careerNumbers[3]}
        rikishiRecords["total"] = careerRecord

        return rikishiRecords


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
