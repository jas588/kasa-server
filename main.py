# main.py

from kasa_device_manager import KasaDeviceManager


if __name__ == "__main__":
    kasaDeviceManager = KasaDeviceManager()
    # kasaDeviceManager.print_devices()
    # kasaDeviceManager.toggle_plug_by_name("family room plug")
    print(kasaDeviceManager.get_devices())
