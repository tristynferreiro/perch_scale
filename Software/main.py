# Import functions
from scale import save_to_file
from rtc import readRTC, firstTimeRTCSetup

counter = 0

while True:
    print(Calibration_factor)
    reading = hx.get_raw_data_mean(10) - hx.get_current_offset()
    calibrated_reading = reading*Calibration_factor
    print("Scale reading: ", reading)
    print("Scale reading with calibration: ", calibrated_reading)
    #print(calibrated_reading/reading)
    save_to_file(counter, calibrated_reading, readRTC()) 
    counter += 1
	#time.sleep(2)
