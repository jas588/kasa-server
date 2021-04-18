from kasa_device_manager import KasaDeviceManager


if __name__ == "__main__":
    kasa_device_manager = KasaDeviceManager()

    # Print all the discovered devices out to the console
    devices = kasa_device_manager.get_all_devices()
    print(devices)

    # Toggle a devices power state
    # kasa_device_manager.toggle_device_by_name("family room plug")