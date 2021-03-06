import asyncio
import kasa
import json


class KasaDeviceManager:
    def __init__(self):
        print("Initializing Kasa Device Manager")
        
        self.devices = self._discover_devices()
        # self._print_devices()

        print("Finished initializing")


    # Private methods
    def _discover_devices(self, json_format=False):        
        discovered_devices = asyncio.run(kasa.Discover.discover(return_raw=json_format))
        
        return discovered_devices

    def _print_devices(self):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())
            print(f"Device: {smart_device}")
            print("--------------------------")

        print("\n")

    def _turn_off_device(self, device: kasa.SmartDevice):
        print(f"Turning {device.alias} off")

        asyncio.run(device.turn_off())

        return True

    def _turn_on_device(self, device: kasa.SmartDevice):
        print(f"Turning {device.alias} on")

        asyncio.run(device.turn_on())

        return True

    def _toggle_device(self, device: kasa.SmartDevice):
        asyncio.run(device.update())

        if device.is_on:
            return self._turn_off_device(device)
        else:
            return self._turn_on_device(device)


    # Public methods
    def get_all_devices(self):
        devices = []

        for ip_address, smart_device in self.devices.items():
            # Update to get the most current state of the device
            asyncio.run(smart_device.update())
            devices.append((smart_device, ip_address))

        return devices

    def rediscover_devices(self):
        self.devices = self._discover_devices()

    def get_device(self, device_name):
        # Find the device and return the most current state of it
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if device_name.lower() == smart_device.alias.lower():
                return smart_device, ip_address

        return None, None

    def toggle_device_by_name(self, device_name):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if device_name.lower() == smart_device.alias.lower():
                return self._toggle_device(smart_device)
        
        return False

    def turn_on_device_by_name(self, device_name):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if device_name.lower() == smart_device.alias.lower():
                return self._turn_on_device(smart_device)
        
        return False

    def turn_off_device_by_name(self, device_name):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if device_name.lower() == smart_device.alias.lower():
                return self._turn_off_device(smart_device)
        
        return False