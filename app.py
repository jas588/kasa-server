from flask import Flask
from flask import Response
from flask import request
from kasa_device_manager import KasaDeviceManager
import json

app = Flask(__name__)
kasa_device_manager = KasaDeviceManager()


# Endpoints
@app.route('/devices')
def get_all_devices():
    """
    Returns all the Kasa devices found in the home.
    /devices
    ---
    GET:
      responses:
        200:
            description: Returns a list of devices
            content: application/json
        404:
            description: Returns when no devices are found
            content: application/json
    """

    link_resources = {"_links": {
        "self": {"href": "/devices"}, 
        "rediscover": {"href": "/devices/rediscover"}
    }}

    found_devices = kasa_device_manager.get_all_devices()

    return format_multiple_devices_response(found_devices, link_resources)

@app.route('/devices/rediscover')
def rediscover_devices():
    """
    Rescans the network for devices and return them.
    /devices/rediscover
    ---
    GET:
      responses:
        200:
            description: Returns a list of devices
            content: application/json
        404:
            description: Returns when no devices are found
            content: application/json
    """

    kasa_device_manager.rediscover_devices()

    link_resources = {"_links": {
        "self": {"href": "/devices/rediscover"}, 
        "all": {"href": "/devices"}
    }}

    found_devices = kasa_device_manager.get_all_devices()

    return format_multiple_devices_response(found_devices, link_resources)

@app.route('/devices/<string:device_name>')
def get_device(device_name):
    """
    Returns the Kasa device
    /devices/entry%20lamp%20plug
    ---
    GET:
      responses:
        200:
            description: Returns the device
            content: application/json
        404:
            description: Returns an error when a device with the specified name is not found
            content: application/json
    """

    found_device, ip_address = kasa_device_manager.get_device(device_name)

    if found_device == None:
        return Response(json.dumps({"error": "no device found"}), status=404, mimetype='application/json')
    else:
        device = format_device(found_device, ip_address)

        headers = {'Access-Control-Allow-Origin': '*'}
        return Response(json.dumps(device), status=200, mimetype='application/json', headers=headers)

@app.route('/devices/<string:device_name>/toggle', methods=['PUT'])
def toggle_device(device_name):   
    """
    Toggle's a Kasa smart device
    devices/entry%20lamp%20plug/toggle
    ---
    PUT:
      responses:
        204:
            description: Returns a no content response upon success
            content: application/json
        404:
            description: Returns an error when a device with the specified name is not found
            content: application/json
    """ 

    toggled = kasa_device_manager.toggle_device_by_name(device_name)
    
    return format_device_power_state_response(toggled)

@app.route('/devices/<string:device_name>/on', methods=['PUT'])
def turn_on_device(device_name):   
    """
    Turns on a Kasa smart device
    /devices/entry%20lamp%20plug/on
    ---
    PUT:
      responses:
        204:
            description: Returns a no content response upon success
            content: application/json
        404:
            description: Returns an error when a device with the specified name is not found
            content: application/json
    """ 

    toggled = kasa_device_manager.turn_on_device_by_name(device_name)

    return format_device_power_state_response(toggled)

@app.route('/devices/<string:device_name>/off', methods=['PUT'])
def turn_off_device(device_name):   
    """
    Turns off a Kasa smart device
    /devices/entry%20lamp%20plug/off
    ---
    PUT:
      responses:
        204:
            description: Returns a no content response upon success
            content: application/json
        404:
            description: Returns an error when a device with the specified name is not found
            content: application/json
    """ 

    toggled = kasa_device_manager.turn_off_device_by_name(device_name)
    
    return format_device_power_state_response(toggled)


# Helper functions
def format_device(device, ip_address):
    url_formatted_device_name = device.alias.replace(' ', '%20')
    device = {
        "name": device.alias, 
        "ip_address": ip_address, 
        "is_on": device.is_on,
        "_links": {
            "self": { "href": f"/devices/{url_formatted_device_name}" },
            "toggle": { "href": f"/devices/{url_formatted_device_name}/toggle" },
            "on": { "href": f"/devices/{url_formatted_device_name}/on" },
            "off": { "href": f"/devices/{url_formatted_device_name}/off" }
        }
    }

    return device

def format_device_power_state_response(response):
    headers = {'Access-Control-Allow-Origin': '*'}

    if not response:
        return Response(json.dumps({"error": "device not found"}), status=404, mimetype='application/json', headers=headers)
    else:
        return Response('', status=204, headers=headers)

def format_multiple_devices_response(devices, general_resources):
    headers = {'Access-Control-Allow-Origin': '*'}

    if len(devices) == 0:
        return Response(json.dumps({"error": "no devices found"}), status=404, mimetype='application/json', headers=headers)
    else:
        embedded_device_resources = []
        for device, ip_address in devices:
            device = format_device(device, ip_address)
            embedded_device_resources.append(device)

        complete_devices_response = {"count": len(embedded_device_resources), **general_resources, "_embedded": {"devices": embedded_device_resources}}

        return Response(json.dumps(complete_devices_response), status=200, mimetype='application/json', headers=headers)