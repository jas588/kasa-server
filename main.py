from kasa_device_manager import KasaDeviceManager


if __name__ == "__main__":
    kasaDeviceManager = KasaDeviceManager()

    # Print all the discovered devices out to the console
    devices = kasaDeviceManager.get_all_devices()
    print(devices)

    # Toggle a devices power state
    # kasaDeviceManager.toggle_device_by_name("family room plug")