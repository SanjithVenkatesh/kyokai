import re, utils.constants as constants
from utils.fetch import fetchBanzuke
from typing import List
from multipledispatch import dispatch
from kyokai.rikishi import Rikishi


class Banzuke:
    def __init__(self, year, month):
        information = self.getBanzuke(year, month)
        self.year = year
        self.month = month
        self.location = information[1]
        self.rikishis = self.parseRikishi(information[2:])

    # ex: {"Makucchi": [r1, r2, r3]}
    def parseRikishi(self, rikishis):
        rikDict = {}
        currentDiv = ""
        for r in rikishis:
            rInfo = r.split()
            if len(rInfo) > 1:
                try:
                    if len(rInfo) == 6 and len(re.findall(r"[A-Z]", rInfo[2])) > 1:
                        splitOriginBeya = re.findall("[A-Z][^A-Z]*", rInfo[2])
                        rikDict[currentDiv].append(
                            Rikishi(
                                rInfo[1],
                                splitOriginBeya[0],
                                splitOriginBeya[1],
                                rInfo[3],
                                rInfo[4],
                                rInfo[5],
                                rInfo[0],
                            )
                        )
                    else:
                        rikDict[currentDiv].append(
                            Rikishi(
                                rInfo[1],
                                rInfo[2],
                                rInfo[3],
                                rInfo[4],
                                rInfo[5],
                                rInfo[6],
                                rInfo[0],
                            )
                        )
                except Exception as e:
                    print(rInfo, "\n", e)
            else:
                currentDiv = rInfo[0].lower()
                rikDict[currentDiv] = []

        return rikDict

    def getBanzuke(self, year, month):
        banzukeText = fetchBanzuke(year, month)
        banzuke = banzukeText.split("<pre>")[1].split("Banzuke Notes")[0]
        banzukeLines = banzuke.split("\n")
        banzukeLines = [
            i.rstrip("\r")
            for i in banzukeLines
            if i is not None and len(i) > 0 and i != "\r"
        ]

        return banzukeLines

    @dispatch(str)
    def _getRikishiByDivision(self, division: str) -> List[Rikishi]:
        rikishi = set()
        for r in self.rikishis[division.lower()]:
            rikishi.add(r)
        return list(rikishi)

    def getRikishiByDivision(self, division) -> List[Rikishi]:
        if type(division) is str:
            return self._getRikishiByDivision(division)
        elif type(division) is int:
            try:
                return self._getRikishiByDivision(constants.DIVISIONS[division - 1])
            except:
                raise Exception(f"Unable to get Rikishi from division {division}!")
        else:
            raise Exception("Invalid division argument type!")

    # Return all Rikishis for a given beya
    def getRikishiByBeya(self, beya) -> List[Rikishi]:
        return [
            rikishi
            for division in self.rikishis.values()
            for rikishi in division
            if rikishi.beya == beya
        ]
