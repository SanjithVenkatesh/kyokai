"""
Test the Rikishi module logic
"""
import sys
sys.path.append('../')

import unittest
from unittest.mock import Mock, patch
from kyokai.utils.date import Debut
from kyokai.rikishi import *
from rikishi_constants import TAKAKEISHO_PAGE

SHIKONA = "Atamifuji"
YEAR, MONTH = 2023, 5

def setup_mock_response(status_code, text):
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.text = text
    return mock_response

class TestRikishi(unittest.TestCase):

    @classmethod
    @patch('kyokai.utils.fetch.requests.get')
    def setUpClass(cls, mock_get):
        mock_response = setup_mock_response(200, TAKAKEISHO_PAGE)
        mock_get.return_value = mock_response
        cls.r = Rikishi(SHIKONA, year=YEAR, month=MONTH)

    def test_rikishi_latest_shikona(self):
        self.assertEqual(self.r.getCurrentShikona(), "Atamifuji Sakutaro")

    def test_rikishi_current_heya(self):
        self.assertEqual(self.r.getCurrentHeya(), "Isegahama")

    def test_rikishi_debut(self):
        correctDate = Debut('2020.11')
        self.assertEqual(self.r.getDebut(), correctDate)
    
    def test_rikishi_career_wins(self):
        self.assertEqual(self.r.getCareerWins(), 134)
    
    def test_rikishi_career_loses(self):
        self.assertEqual(self.r.getCareerLoses(), 76)

    def test_rikishi_division_wins(self):
        correctWins = {"Makuuchi": 26, "Juryo": 68, "Makushita": 21, "Sandanme": 6, "Jonidan": 7, "Jonokuchi": 6}
        for division in correctWins.keys():
            self.assertEqual(self.r.getDivisionWins(division), correctWins[division])

    def test_rikishi_division_loses(self):
        correctLoses = {"Makuuchi": 19, "Juryo": 48, "Makushita": 7, "Sandanme": 1, "Jonidan": 0, "Jonokuchi": 1}
        for division in correctLoses.keys():
            self.assertEqual(self.r.getDivisionLoses(division), correctLoses[division])

if __name__ == '__main__':
    unittest.main()