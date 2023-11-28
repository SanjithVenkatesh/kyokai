"""
Test the fetch utility module
"""

import sys
sys.path.append("../")

import unittest
from unittest.mock import Mock, patch
from kyokai.utils.fetch import fetchRikishi, fetchBanzuke, fetchTorikumi
from kyokai.utils.exceptions import NoTorikumiFoundError, NoBanzukeFoundError, FetchURLError, NeedDayForTorikumiFetchError
import kyokai.utils.constants as constants

SHIKONA, YEAR, MONTH, DAY = "Takakeisho", 2023, 11, 1

def setup_mock_response(status_code, text):
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.text = text
    return mock_response

class TestFetch(unittest.TestCase):

    @patch('kyokai.utils.fetch.requests.get')
    def test_fetch_rikishi(self, mock_get):
        mock_response = setup_mock_response(200, "Some Rikishi")
        mock_get.return_value = mock_response

        result = fetchRikishi(SHIKONA, YEAR, MONTH)

        mock_get.assert_called_once_with(f"{constants.BASE_URL}/Rikishi.aspx?b=202311&shikona=Takakeisho")
        self.assertEqual(result, "Some Rikishi")
    
    @patch('kyokai.utils.fetch.requests.get')
    def test_fetch_banzuke(self, mock_get):
        mock_response = setup_mock_response(200, "<pre>Some Banzuke")
        mock_get.return_value = mock_response

        result = fetchBanzuke(YEAR, MONTH)

        mock_get.assert_called_once_with(f"{constants.BASE_URL}/Banzuke_text.aspx?b=202311")
        self.assertEqual(result, "<pre>Some Banzuke")
    
    @patch('kyokai.utils.fetch.requests.get')
    def test_fetch_torikumi(self, mock_get):
        mock_response = setup_mock_response(200, "<pre>Some Torikumi")
        mock_get.return_value = mock_response

        result = fetchTorikumi(YEAR, MONTH, DAY)

        mock_get.assert_called_once_with(f"{constants.BASE_URL}/Results_text.aspx?b=202311&d=1")
        self.assertEqual(result, "<pre>Some Torikumi")
    
    @patch('kyokai.utils.fetch.requests.get')
    def test_fetch_torikumi_no_torikumi_found(self, mock_get):
        mock_response = setup_mock_response(200, "Some Torikumi")
        mock_get.return_value = mock_response

        with self.assertRaises(NoTorikumiFoundError):
            fetchTorikumi(YEAR, MONTH, DAY)

        mock_get.assert_called_once_with(f"{constants.BASE_URL}/Results_text.aspx?b=202311&d=1")
    
    def test_fetch_torikumi_day_is_none(self):

        with self.assertRaises(NeedDayForTorikumiFetchError):
            fetchTorikumi(YEAR, MONTH, None)
    
    def test_fetch_torikumi_no_day_provided(self):

        with self.assertRaises(NeedDayForTorikumiFetchError):
            fetchTorikumi(YEAR, MONTH)
    
    
    @patch('kyokai.utils.fetch.requests.get')
    def test_fetch_banzuke_no_banzuke_found(self, mock_get):
        mock_response = setup_mock_response(200, "Some Banzuke")
        mock_get.return_value = mock_response

        with self.assertRaises(NoBanzukeFoundError):
            fetchBanzuke(YEAR, MONTH)

        mock_get.assert_called_once_with(f"{constants.BASE_URL}/Banzuke_text.aspx?b=202311")

    @patch('kyokai.utils.fetch.requests.get')
    def test_fetch_rikishi_fail_fetch_data(self, mock_get):
        mock_response = setup_mock_response(404, "No Rikishi")
        mock_get.return_value = mock_response

        with self.assertRaises(FetchURLError):
            fetchRikishi(SHIKONA, YEAR, MONTH)
        
        mock_get.assert_called_once_with(f"{constants.BASE_URL}/Rikishi.aspx?b=202311&shikona=Takakeisho")


if __name__ == "__main__":
    unittest.main()
