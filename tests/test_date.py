"""
Test Date module and its incorporated classes
"""

import sys
sys.path.append('../')

import unittest
from kyokai.utils.date import Date
from kyokai.utils.exceptions import *

class TestDate(unittest.TestCase):

    def test_date_init(self):
        d = Date(2002, 2, 12)
        self.assertEqual(d.year, 2002)
        self.assertEqual(d.month, 2)
        self.assertEqual(d.day, 12)
    
    def test_date_init_day_non(self):
        d = Date(2002, 12)
        self.assertEqual(d.year, 2002)
        self.assertEqual(d.month, 12)
        self.assertEqual(d.day, None)
    
    def test_date_invalid_day(self):
        self.assertRaises(InvalidMonthError,
                          Date, 2002, 13, 1)
    
    def test_leap_year_invalid_day(self):
        self.assertRaises(LeapYearDayInvalidError,
                          Date, 2000, 2, 30)
    
    def test_invalid_days_of_month(self):
        self.assertRaises(InvalidDayForMonthError,
                          Date, 2000, 4, 31)
