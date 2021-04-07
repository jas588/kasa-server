# app.py

from flask import Flask
from flask import Response
from flask import request
from kasa_device_manager import KasaDeviceManager
import json

app = Flask(__name__)
kasaDeviceManager = KasaDeviceManager()


@app.route('/devices')
def get_devices():
    """
    Returns all the Kasa devices found in the home.
    ---
    GET:
      description: Get all Kasa devices
      responses:
        200:
          description: Returns a list of devices
          content:
            application/json:
              schema: {"devices": [{"name": string, "ip_address": string, "is_on": boolean}]}
        404:
            description: Returns when no devices are found
            content:
                application/json:
                schema: {"error": string}
    """

    devices = kasaDeviceManager.get_devices()

    if len(devices['devices']) == 0:
        return Response(json.dumps({"error": "no devices found"}), status=404, mimetype='application/json')
    else:
        return Response(json.dumps(devices), status=200, mimetype='application/json')

@app.route('/toggle/device/<string:device_name>')
def toggle_device(device_name):   
    """
    Toggle's a Kasa smart device.
    http://127.0.0.1:5000/toggle/device/entry%20lamp%20plug
    ---
    GET:
      description: Toggle's the smart device
      responses:
        204:
          description: Returns a no content response upon success
        404:
            description: Returns when a device with that name is not found
            content:
                application/json:
                schema: {"error": string}
    """ 

    device_name2 = request.args.get('name')

    print("Query params: ", device_name2)

    response = kasaDeviceManager.toggle_device_by_name(device_name)

    if not response:
        return Response(json.dumps({"error": "device not found"}), status=404, mimetype='application/json')
    else:
        return Response('', status=204)