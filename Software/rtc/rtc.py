import smbus
import time
from datetime import datetime, timedelta
import SDL_DS3231
from os.path import exists
import subprocess
import os

def checkI2CState():
    result = subprocess.run(["sudo","raspi-config","nonint","get_i2c"],capture_output=True,text=True)
    if result.returncode == 0:
        output = result.stdout.strip()
        if output == '1':
            print("I2C currently disabled")
            return False
        elif output == '0':
            print("I2C currently enabled")
            return True
            
def enableI2C():            
    result = subprocess.run(["sudo","raspi-config","nonint","do_i2c","0"],capture_output=True,text=True)
    if result.returncode == 0:
        print("Sucesfully enabled I2C")
        return True
    else:
        return False

def disableI2C():            
    result = subprocess.run(["sudo","raspi-config","nonint","do_i2c","1"],capture_output=True,text=True)
    if result.returncode == 0:
        print("Sucesfully disabled I2C")
        return True
    else:
        return False
        
def RTCDetect():            
    result = subprocess.run(["sudo","i2cdetect","-y","1"],capture_output=True,text=True)
    if result.returncode == 0:
        result_str = f"stdout: {result.stdout}\nstderr: {result.stderr}"
        if '68' in result_str:
            print("RTC module detected")
            return True
        if 'UU' in result_str:
            print("RTC module busy")
            resetI2CPort()
            RTCDetect()
    else:
        return False
        
def resetI2CPort():
    try:
        subprocess.run(["sudo","rmmod","rtc_ds1307"],check=True)
        print("Restarted I2C interface for RTC")
        return True
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
        
    
def addRTC():
    try:
        subprocess.run(["sudo","modprobe","rtc-ds1307"],check=True)
        # print("ran first command")
        subprocess.run(["sudo","bash","-c","echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print("Succesfuly added RTC as new device")
        return True
        
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
        
def checkRTC():
    RTCDetect()
    result = subprocess.run(["sudo","hwclock","-r"],capture_output=True,text=True)
    if result.returncode == 0:
        print("RTC can be read from :)")
        return True
    else:
        return False
        
def firstTimeWriteRTC():
    result = subprocess.run(["sudo","hwclock","-w"],check=True)
    if result.returncode == 0:
        print("Succesfully wrote device time to RTC")
        return True
    else:
        return False
        
def setRTCAsClock():
    try:
        with  open("/etc/modules","a") as f:
            f.write("rtc-ds1307\n")
            
        with open("/etc/rc.local","r") as f:
            lines = f.readlines()
            
        if "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device\n" not in lines:
            lines.insert(-2,"echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device\n")
        if "sudo hwclock -s\n" not in lines:
            lines.insert(-2,"sudo hwclock -s\n")
            
        with open("/etc/rc.local","w") as f:
            f.writelines(lines)
                
        print("Succesfully set RTC as device clock")
        return True
        
    except Exception as e:
        return f"Error: {e}"
        
def upDirectory():
    cd = os.getcwd()
    if cd != '/home/raspberry/':
        os.chdir('..')
        return True
    else:
        return False
        

### Function to create a file object with the input function name
def createFile(filename):
    time_file = open(filename,"w")
    return time_file

### Function to write to an existing file. If not exist, create
def writeToFile(filename):
    if exists(filename):
        time_file = open(filename,"w")
        return time_file
    createFile(filename)
    writeToFile(filename)
    
def readRTC():
    '''
    Function to read the RTC clock and return a string
    '''
    # Read the RTC I2C address using library
    ds3231 = SDL_DS3231.SDL_DS3231(1,0x68)
    t = ds3231.read_datetime() # Get UTC time
    t = t + timedelta(hours=2) # Convert to SAST
    # print(t)
    # Convert to string of desired format
    t_str = t.strftime("%m/%d/%Y %H:%M:%S")
    return t_str
    
def firstTimeRTCSetup():
    i2c_status = checkI2CState()
    if i2c_status:
        print("I2C enabled")
        upDirectory()
        addRTC()
        firstTimeWriteRTC()
        setRTCAsClock()
        checkRTC()
        print("RTC can be read from")
        print("Current RTC time (SAST):",readRTC())       
        
    else:
        enableI2C()
        print("I2C succesfully enabled")
        firstTimeRTCSetup()    
        
   
#firstTimeRTCSetup() 
print(readRTC())
    
    
'''
# Set file to write time data to
file_time = writeToFile("time.txt")
# Set the number of values to take (Testing line)
vals = int (input("How many readings should be taken?: "))
# Every how many seconds (Testing line)
sleep_time = int (input("Every how many seconds?: "))
i=0

while i<=vals:
    # Read the RTC I2C address using library
    ds3231 = SDL_DS3231.SDL_DS3231(1,0x68)
    t = ds3231.read_datetime() # Get UTC time
    t = t + timedelta(hours=2) # Convert to SAST
    print(t)
    # Convert to string of desired format
    t_str = t.strftime("%m/%d/%Y, %H:%M:%S")
    # Write to file
    file_time.write(t_str)
    time.sleep(sleep_time)
    i =i+1
# Close file
file_time.close()
'''
