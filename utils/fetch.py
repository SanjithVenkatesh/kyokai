"""
Functions to perform REST calls
"""
import requests, utils.constants as constants
from utils.exceptions import (
    FetchURLError,
    NoBanzukeFoundError,
    NoTorikumiFoundError,
    NeedDayForTorikumiFetchError,
)


texts = {"banzuke": "Banzuke", "torikumi": "Results", "rikishi": "Rikishi"}


def _fetchInfo(type: str, year: int, month: int, **kwargs):
    type = type.lower()
    monthStr = f"0{month}" if month < 10 else f"{month}"
    banzuke = f"{year}{monthStr}"

    if type == "torikumi" and kwargs["day"] is None:
        raise NeedDayForTorikumiFetchError(year, month, kwargs["day"])

    url = f"{constants.BASE_URL}/{texts[type]}_text.aspx?b={banzuke}"
    if type == "rikishi":
        url = url.replace("_text", "")

    if type == "torikumi" and "day" in kwargs and kwargs["day"]:
        dayStr = kwargs["day"]
        url += f"&d={dayStr}"
    if type == "rikishi" and "shikona" in kwargs and kwargs["shikona"]:
        shikonaStr = kwargs["shikona"]
        url += f"&shikona={shikonaStr}"

    print("URL: ", url)

    rText = _fetchData(url)

    if "<pre>" not in rText and type != "rikishi":
        if type == "torikumi":
            raise NoTorikumiFoundError(year, month, kwargs["day"])
        else:
            raise NoBanzukeFoundError(year, month)

    return rText


def fetchBanzuke(year, month):
    return _fetchInfo("banzuke", year, month)


def fetchTorikumi(year, month, day):
    return _fetchInfo("torikumi", year, month, day=day)


def fetchRikishi(shikona, year, month):
    return _fetchInfo("rikishi", year, month, shikona=shikona)


def _fetchData(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise FetchURLError(url)
    return r.text
