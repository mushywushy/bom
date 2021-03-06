# app.py
import json
import logging
import requests

from flask import Flask, request, jsonify, Response, abort

import bomlib.helpers as helpers

app = Flask(__name__)


@app.errorhandler(503)
def error_service_unavailable(e):
    return jsonify(error=str(e)), 503


@app.route('/raw')
def view_raw():
    """
        View: /raw
        A debug viewpoint. Display the BOM data in its rawest form.
    """
    bom_json = None
    try:
        bom_response = requests.get(helpers.BOM_URL)
        bom_response.raise_for_status()
        bom_json = bom_response.json()
    except requests.exceptions.HTTPError as error:
        app.logger.error(error)
        abort(503, description="Error Connecting to BOM: %s" % str(error))
    return jsonify(bom_json)


@app.route('/')
def index():
    """
        View: /
        Display specific BOM data, showing only data where 'apparent_t' > 20
        The data fields we want are:
            "name",
            "apparent_t",
            "lat",
            "long",
    """

    # Connect to BOM, and get the raw data
    bom_json = None
    try:
        bom_response = requests.get(helpers.BOM_URL)
        bom_response.raise_for_status()
        bom_json = bom_response.json()
    except requests.exceptions.HTTPError as error:
        app.logger.error(error)
        abort(503, description="Error Connecting to BOM: %s" % str(error))

    # Handle an optional temperature argument
    temperature = request.args.get('temperature')
    if temperature is not None:
        try:
            temperature = float(temperature)
        except:
            temperature = None
    if temperature is None:
        temperature = 20  # default value

    # Get the BOM stations
    stations = bom_json["observations"]["data"]

    # Filter out for the stations we are interested in
    # Assumes that apparent_t provided is an int
    stations_we_want = [ station for station in stations if station["apparent_t"] > temperature ]
    app.logger.debug("Showing %s/%s stations, where temperature > %s", len(stations_we_want), len(stations), temperature)

    # Build the response data, keyed by apparent_t to allow sorting
    sorted_stations = []
    for station in stations_we_want:
        # Get the data we are interested in
        name = station["name"]
        apparent_t = station["apparent_t"]
        lat = station["lat"]
        lon = station["lon"]

        # Build the response object for this station
        d = {
            "name": name,
            "apparent_t": apparent_t,
            "lat": lat,
            "lon": lon,
        }

        # Append to the data list, allowing us to sort later
        sorted_stations.append((apparent_t, d))

    # And sort. Default is ascending
    sorted_stations.sort()

    # Return response data
    return jsonify([ station for (key, station) in sorted_stations ])


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host='0.0.0.0', threaded=True, port=5000)
