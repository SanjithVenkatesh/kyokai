from kyokai.banzuke import Banzuke
from kyokai.torikumi import Torikumi
from kyokai.rikishi import Rikishi
import utils.constants as constants
from utils.birthDate import birthDate

def main():
    year = 2018
    month = 5
    day = 1
    shikona = "Aoiyama"
    birthStr = 'March 2, 1999 (24 years)'

    # bd = birthDate(birthStr)
    # print(bd.getAge())
    r = Rikishi(shikona, year=year, month=month)
    # b = Banzuke(year, month)
    # t = Torikumi(year, month, day)
    #print(t.matches)
    # for division, bouts in t.matches.items():
    #     for bout in bouts:
    #         print(division, bout.getWinner())
    # print(constants.KIMARITES)

    # # print(b.getDivisionRikishi("Makuuchi"))
    # print(b.getRikishiByDivision(1))


if __name__ == "__main__":
    main()