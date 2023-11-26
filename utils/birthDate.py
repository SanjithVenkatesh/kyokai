"""
Utility class to represent the birth date of a Rikishi
"""
from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class birthDate:

    # Example string: March 2, 1999 (24 years)
    def __init__(self, ageString: str):
        ageStringSplit = ageString.split()
        self.month, self.day, self.year = months.index(ageStringSplit[0]) + 1, int(ageStringSplit[1][:-1]), int(ageStringSplit[2])
    
    # Get the age in simply terms of years based on the computer's current time and date
    def getAge(self):
        birth = datetime(self.year, self.month, self.day)
        age = datetime.utcnow() - birth
        return int(age.total_seconds() / 31556926)