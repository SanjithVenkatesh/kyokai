class FetchURLError(Exception):
    BASE_MESSAGE = "Cannot fetch data from URL!\nURL: "

    def __init__(self, url, message=BASE_MESSAGE):
        self.url = url
        self.message = f"{message}{self.url}"
        super().__init__(self.message)

class NoBanzukeFoundError(Exception):
    BASE_MESSAGE = "Banzuke cannot be found!"

    def __init__(self, year, month, message=BASE_MESSAGE):
        self.year, self.month = year, month
        self.message = f"{message}\nYear = {self.year} Month: {self.month}"
        super().__init__(self.message)

class NoTorikumiFoundError(Exception):
    BASE_MESSAGE = "Torikumi cannot be found!"

    def __init__(self, year, month, day, message=BASE_MESSAGE):
        self.year, self.month, self.day = year, month, day
        self.message = f"{message}\nYear = {self.year} Month: {self.month} Day: {self.day}"
        super().__init__(self.message)

class NeedDayForTorikumiFetchError(Exception):
    BASE_MESSAGE = "Torikumi requires a day!"

    def __init__(self, year, month, day, message=BASE_MESSAGE):
        self.year, self.month, self.day = year, month, day
        self.message = f"{message}\nYear = {self.year} Month: {self.month} Day: {self.day}"
        super().__init__(self.message)

class RikishiNotFoundError(Exception):
    BASE_MESSAGE = "Rikishi could not be found!"

    def __init__(self, shikona, year, month, message=BASE_MESSAGE):
        self.shikona, self.year, self.month, self.day = shikona, year, month
        self.message = f"{message}\nShikona: {self.shikona} Year = {self.year} Month: {self.month}"
        super().__init__(self.message)