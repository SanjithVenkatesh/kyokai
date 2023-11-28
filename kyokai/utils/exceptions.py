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
        self.message = (
            f"{message}\nYear = {self.year} Month: {self.month} Day: {self.day}"
        )
        super().__init__(self.message)


class NeedDayForTorikumiFetchError(Exception):
    BASE_MESSAGE = "Torikumi requires a day!"

    def __init__(self, year, month, day, message=BASE_MESSAGE):
        self.year, self.month, self.day = year, month, day
        self.message = (
            f"{message}\nYear = {self.year} Month: {self.month} Day: {self.day}"
        )
        super().__init__(self.message)


class RikishiNotFoundError(Exception):
    BASE_MESSAGE = "Rikishi could not be found!"

    def __init__(self, shikona, year, month, message=BASE_MESSAGE):
        self.shikona, self.year, self.month = shikona, year, month
        self.message = (
            f"{message}\nShikona: {self.shikona} Year = {self.year} Month: {self.month}"
        )
        super().__init__(self.message)

class InvalidMonthError(Exception):
    BASE_MESSAGE = "Month is not valid!"

    def __init__(self, month, message=BASE_MESSAGE):
        self.month =month
        self.message = (
            f"{message}\tMonth: {self.month}"
        )
        super().__init__(self.message)

class LeapYearDayInvalidError(Exception):
    BASE_MESSAGE = "Leap year day is invalid!"

    def __init__(self, year, day, message=BASE_MESSAGE):
        self.year, self.day = year, day
        self.message = (
            f"{message}\Year: {self.year}, Day: {self.day}"
        )
        super().__init__(self.message)

class InvalidDayForMonthError(Exception):
    BASE_MESSAGE = "Day isn't valid with Month!"

    def __init__(self, month, day, message=BASE_MESSAGE):
        self.month, self.day = month, day
        self.message = (
            f"{message}\Month: {self.month}, Day: {self.day}"
        )
        super().__init__(self.message)
