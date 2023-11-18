from kyokai.banzuke import Banzuke
from kyokai.torikumi import Torikumi
import utils.constants as constants

def main():
    year = 2023
    month = 5
    day = 1
    # b = Banzuke(year, month)
    t = Torikumi(year, month, day)
    #print(t.matches)
    for division, bouts in t.matches.items():
        for bout in bouts:
            print(division, bout.getWinner())
    # print(constants.KIMARITES)

    # # print(b.getDivisionRikishi("Makuuchi"))
    # print(b.getRikishiByDivision(1))


if __name__ == "__main__":
    main()