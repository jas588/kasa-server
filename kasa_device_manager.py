# kasa_device_manager.py

import asyncio
import kasa
import json


class KasaDeviceManager:
    def __init__(self):
        print("Initializing Kasa Device Manager")
        
        self.devices = self._discover_devices()
        # self._print_devices()

        print(f"Finished initializing")


    # Private methods
    def _discover_devices(self, json=False):        
        devices = asyncio.run(kasa.Discover.discover(return_raw=json))
        
        return devices


    def _print_devices(self):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())
            print(f"Device: {smart_device}")
            print("--------------------------")

        print("\n")


    def _turn_off_plug(self, plug: kasa.SmartPlug):
        print(f"Turning {plug.alias} off")

        asyncio.run(plug.turn_off())

        return {"name": plug.alias, "state": "off"}

    def _turn_on_plug(self, plug: kasa.SmartPlug):
        print(f"Turning {plug.alias} on")

        asyncio.run(plug.turn_on())

        return {"name": plug.alias, "state": "on"}

    def _toggle_plug(self, plug: kasa.SmartPlug):
        asyncio.run(plug.update())

        if plug.is_on:
            return self._turn_off_plug(plug)
        else:
            return self._turn_on_plug(plug)


    # Public methods
    def get_devices(self):
        minified_devices = []

        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())
            minified_device = {"name": smart_device.alias, "ip_address": ip_address, "is_on": smart_device.is_on}
            minified_devices.append(minified_device)

        devices = {"devices": minified_devices} # TODO: Make Flask function handle error
        return devices


    def toggle_plug_by_ip(self, ip_address):
        plug = kasa.SmartPlug(ip_address)
        asyncio.run(plug.update())

        if plug.is_on:
            return self._turn_off_plug(plug)
        else:
            return self._turn_on_plug(plug)


    def toggle_plug_by_name(self, alias_name):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if alias_name.lower() == smart_device.alias.lower():
                return self._toggle_plug(smart_device)
        
        return {"status": "not_found"}
