"""
Functions to perform REST calls
"""
import requests, constants
from exceptions import FetchURLError, NoBanzukeFoundError, NoTorikumiFoundError, NeedDayForTorikumiFetchError


texts = {"banzuke": "Banzuke", "torikumi": "Results"}

def _fetchInfo(type: str, year: int, month: int, day: str=None):
    type = type.lower()
    monthStr = f"0{month}" if month < 10 else f"{month}"
    banzuke = f"{year}{monthStr}"
    if type is "torikumi" and day is None:
        raise NeedDayForTorikumiFetchError(year, month, day)
    url = f"{constants.BASE_URL}/{texts[type]}_text.aspx?b={banzuke}"
    if type == 'torikumi' and day is not None:
        url += f"&d={day}"
    print("URL: ", url)
    rText = _fetchData(url)
    if "<pre>" not in rText:
        if type == "torikumi":
            raise NoTorikumiFoundError(year, month, day)
        else:
            raise NoBanzukeFoundError(year, month)
    return rText

def fetchBanzuke(year, month):
    return _fetchInfo("banzuke", year, month)

def fetchTorikumi(year, month, day):
    return _fetchInfo("torikumi", year, month, day)


def _fetchData(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise FetchURLError(url)
    return r.text