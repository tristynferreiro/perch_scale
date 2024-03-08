from rtc import *
import time

def setupWiFi():
	if wifiEnabledCheck():
		if networkConnectedCheck():
			while not internetAccess():
				print("Failed to connect to the internet. Retrying...")
				internetAccess()
		if internetAccess():
			print("WiFi is enabled, and connected to internet")
			return True				
	else:
		while not connectToNetwork():
			print("Failed to connect to WiFi network. Retrying...")
			setupWiFi()
				

if __name__ == '__main__':
	print("Please ensure your Hotspot is on with the following details:\nNetwork Name: Hotspot \t Password:password")
	print("Now setting up RTC on Pi")
	time.sleep(10)
	wifi_status = setupWiFi()
	if wifi_status:
		firstTimeRTCSetup()
		if firstTimeRTCSetup():
			print("RTC is succesfully setup and enabled.\nThe current time is:",readRTC())
			print("You can now disable your hotspot")
			turnOffWiFi()
