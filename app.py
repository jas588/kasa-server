# app.py

from flask import Flask
from kasa_device_manager import KasaDeviceManager


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
    """
    return kasaDeviceManager.get_devices()

@app.route('/toggle/plug/<string:plug_name>')
def toggle_plug(plug_name):   
    """
    Toggle's a Kasa smart plug.
    http://127.0.0.1:5000/toggle/plug/entry%20lamp%20plug
    ---
    GET:
      description: Toggle's the smart plug
      responses:
        200:
          description: Returns whether the request was a success or failure 
          content:
            application/json:
              schema: {"status": string}
    """ 
    response = kasaDeviceManager.toggle_plug_by_name(plug_name)
    return response