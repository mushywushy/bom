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
        """
        bom_response = requests.get(helpers.BOM_URL)
        self.assertEqual(bom_response.status_code, 200)

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


