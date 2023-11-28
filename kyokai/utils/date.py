"""
Utility class to represent the birth date of a Rikishi
"""
from datetime import datetime
from .exceptions import InvalidMonthError, LeapYearDayInvalidError, InvalidDayForMonthError

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DIM = {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31, 'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}

class Date:
    
    def __init__(self, year, month, day=None):
        self.year, self.month, self.day = year, month, day
        if self.month < 1 or self.month > 12:
            raise InvalidMonthError(self.month)
        if self.month == 2 and self.year % 4 == 0 and self.day > 29:
            raise LeapYearDayInvalidError(self.year, self.day)
        if self.day and self.day > DIM[months[self.month-1]]:
            raise InvalidDayForMonthError(self.month, self.day)

    def __str__(self):
        return f"Year: {self.year}, Month: {self.month}, Day: {self.day}"

    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day

class BirthDate(Date):

    # Example string: March 2, 1999 (24 years)
    def __init__(self, ageString: str):
        ageStringSplit = ageString.split()
        month, day, year = months.index(ageStringSplit[0]) + 1, int(ageStringSplit[1][:-1]), int(ageStringSplit[2])
        super().__init__(year, month, day)
    
    # Get the age in simply terms of years based on the computer's current time and date
    def getAge(self):
        birth = datetime(self.year, self.month, self.day)
        age = datetime.utcnow() - birth
        return int(age.total_seconds() / 31556926)

class Debut(Date):

    # Example string: "2014.11"
    def __init__(self, debutStr: str):
        debutStrSplit = debutStr.split('.')
        year, month = int(debutStrSplit[0]), int(debutStrSplit[1])
        super().__init__(year, month)

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month