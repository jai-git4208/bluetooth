import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from plyer import bluetooth
from plyer.utils import platform
from android.permissions import request_permissions, Permission

class BluetoothApp(App):
    def build(self):
        # Set up UI layout
        layout = BoxLayout(orientation='vertical')
        
        # Scan button
        self.scan_button = Button(text="Scan for Bluetooth Devices", on_press=self.scan_bluetooth_devices)
        layout.add_widget(self.scan_button)
        
        # Result button
        self.result_button = Button(text="Show Result", on_press=self.show_result)
        layout.add_widget(self.result_button)
        
        # Label to display scanned devices
        self.result_label = Label(text="Scan Results will appear here.")
        layout.add_widget(self.result_label)
        
        # List to store scanned devices
        self.devices = []
        
        # Request permissions if on Android
        if platform == 'android':
            self.request_bluetooth_permissions()
        
        return layout

    def request_bluetooth_permissions(self):
        # Request Bluetooth permissions if not granted
        try:
            request_permissions([Permission.BLUETOOTH, Permission.BLUETOOTH_ADMIN, Permission.ACCESS_FINE_LOCATION])
        except Exception as e:
            print(f"Permission Request Error: {e}")
    
    def scan_bluetooth_devices(self, instance):
        # Function to scan Bluetooth devices
        if platform == 'android':
            try:
                bluetooth.scan_devices(self.on_bluetooth_devices_scanned)
                self.result_label.text = "Scanning for devices..."
            except AttributeError:
                print("Bluetooth scanning is not supported or permissions are missing.")
                self.result_label.text = "Error: Bluetooth scanning not supported."

    def on_bluetooth_devices_scanned(self, devices):
        # Callback function when Bluetooth devices are scanned
        if devices:
            self.devices = devices  # Store scanned devices in the list
            self.result_label.text = "Devices Found:\n" + "\n".join([f"{device['name']} ({device['address']})" for device in self.devices])
        else:
            self.result_label.text = "No devices found."

    def show_result(self, instance):
        # Display the scanned devices
        if self.devices:
            result = "\n".join([f"{device['name']} ({device['address']})" for device in self.devices])
            print("Devices Found:", result)
        else:
            self.result_label.text = "No devices found."

if __name__ == "__main__":
    BluetoothApp().run()