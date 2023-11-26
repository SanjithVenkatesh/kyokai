from utils.fetch import fetchTorikumi
from typing import Dict
from collections import Counter, defaultdict
import utils.constants as constants

"""
This module provides logic for creating a Torikumi object which is a representation of a tournament's day schedule and results
Ex: https://sumodb.sumogames.de/Results.aspx

A torikumi in itself is just a sumo bout, but for our purposes it refers to a day's bout schedule and results
"""


class Bout:
    def __init__(self, winner: str, loser: str, kimarite=None):
        self.winner, self.loser, self.kimarite = winner, loser, kimarite

    def getWinner(self):
        return self.winner if self.kimarite is not None else None


class Torikumi:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.matches = self.processMatches(year, month, day)

    def processMatches(self, year: int, month: int, day: int) -> Dict[str, Bout]:
        torikumi = fetchTorikumi(year, month, day)
        torikumiLines = torikumi.split("<pre>")[1].split("</pre>")[0].split("\n")[2:]
        torikumiLines = [
            i.rstrip("\r") for i in torikumiLines if len(i) > 0 and i != "\r"
        ]
        matches = defaultdict(list)
        currentDivision = None
        for i, v in enumerate(torikumiLines):
            if v in constants.DIVISIONS:
                currentDivision = v
            else:
                splitValue = v.split()
                if len(splitValue) > 0:
                    splitLine = v.split()
                    kimariteInter = Counter(constants.KIMARITES) & Counter(splitLine)
                    if len(kimariteInter) > 0:
                        winner, kimarite, loser = (
                            splitLine[0:3],
                            splitLine[3],
                            splitLine[4:],
                        )
                        matches[currentDivision].append(
                            Bout(winner[1], loser[1], kimarite)
                        )
                    else:
                        winner, loser = splitLine[0:3], splitLine[3:]
                        matches[currentDivision].append(Bout(winner[1], loser[1], None))
        return matches
