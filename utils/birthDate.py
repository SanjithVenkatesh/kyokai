"""
Utility class to represent the birth date of a Rikishi
"""
from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class Date:
    
    def __init__(self, year, month, day=None):
        self.year, self.month, self.day = year, month, day
    
    def __str__(self):
        return f"Year: {self.year}, Month: {self.month}, Day: {self.day}"

    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"

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
        year, month = debutStrSplit[0], debutStrSplit[1]
        super().__init__(year, month)