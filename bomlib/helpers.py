import json
from flask import jsonify

BOM_URL = "http://www.bom.gov.au/fwo/IDN60801/IDN60801.95765.json"


def get_error_message():
    """
        Prepare a default JSON response
        This should be used in the event of an error connecting to BOM
    """
    return jsonify( { "error": "Error Connecting to BOM" } )
