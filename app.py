# app.py

from flask import Flask
from kasa_device_manager import KasaDeviceManager


app = Flask(__name__)
kasaDeviceManager = KasaDeviceManager()

@app.route('/devices')
def get_devices():
    return kasaDeviceManager.get_devices()

# http://127.0.0.1:5000/toggle/plug/entry%20lamp%20plug
@app.route('/toggle/plug/<string:plug_name>')
def toggle_plug(plug_name):    
    print(plug_name)
    response = kasaDeviceManager.toggle_plug_by_name(plug_name)
    return response