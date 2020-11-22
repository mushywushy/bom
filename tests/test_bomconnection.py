import logging
import unittest
import bomlib.helpers as helpers
import requests

logger = logging.getLogger(__name__)


class TestBomConnection(unittest.TestCase):
    def test_verifySuccessfulBomConnection(self):
        """
            Test that a successful BOM connection can be made
            This test may unexpectedly fail if the BOM system is down

            While we are here, check some basic elements within the response data
        """
        bom_response = requests.get(helpers.BOM_URL)
        self.assertEqual(bom_response.status_code, 200)
        bom_json = bom_response.json()

        # While we are here, check that we can see the station data
        self.assertIn("observations", bom_json)
        self.assertIn("data", bom_json["observations"])
        stations = bom_json["observations"]["data"]

        # A safe bet is to ensure that there is at LEAST one station
        self.assertGreaterEqual(len(stations), 1)
        station = stations[0]
        self.assertIn("name", station)
        self.assertIn("apparent_t", station)
        self.assertIn("lat", station)
        self.assertIn("lon", station)

    def test_verifyFailedBomConnection(self):
        """
            Test that an unsuccessful BOM connection can be detected
        """
        try:
            bom_response = requests.get("%s.thisshouldfail.json" % helpers.BOM_URL)
            bom_response.raise_for_status()
            self.fail("This should've returned an error")
        except requests.exceptions.HTTPError as error:
            pass


