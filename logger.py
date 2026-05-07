import sensors_manager
import time_manager
import sd
import os
from lib import files

LOG_DIR = const("/sd/log")

def start(ignored = False):
    try:
        print("Starting Logger Module")
        if not sd.isAvailable():
            raise ValueError("SD card not available")
        
        if not files.dirExists(LOG_DIR):
            print("Log directory probably doesn't exist, creating it.")
            os.mkdir("/sd/log")
            
        logInfo("INFO", "Logging is ready")
    except Exception as e:
        if ignored:
            print("Ignored module caught an error: ", e)
        else:
            raise e
        
def now() -> tuple:
    return time_manager.getRealLocaltime()

def logData(data: sensors_manager.LiveData):
    
    if not isAvailable(): return

    # CSV format is the following:
    # "Time","Moisture","Temperature","Humidity","Infrared","Watering?","BatteryLevel"
    out = ""
    out += _formatTime(now()) + ","

    out += str(data.moisture) + ","
    out += str(data.temperature) + ","
    out += str(data.humidity) + ","
    out += str(data.infrared) + ","
    out += str("n/a") + ","
    out += str(data.battery)

    nametarget = LOG_DIR + "/" + _formatDate(now()) + "-data.csv"

    try:
        os.stat(nametarget)
    except OSError:
        _createDataFile(now())
        logInfo("INFO", "Created data file")

    file = open(nametarget, "a")
    file.write(out)
    file.write("\n")
    file.close()

def logInfo(tag: str, msg: str):

    if not isAvailable(): return
    
    out = ""
    out += "[{}] ".format(_formatTime(now()))
    out += " {} - ".format(tag)
    out += msg

    nametarget = LOG_DIR + "/" + _formatDate(now()) + "-info.csv"
    print("logInfo called: " + nametarget)

    try:
        os.stat(nametarget)
    except OSError:
        _createInfoFile(now())
        logInfo("INFO", "Created info file")

    file = open(nametarget, "a")
    file.write(out)
    file.write("\n")
    file.close()

def _formatTime(time: tuple) -> str:
    return "{3:02d}:{4:02d}:{5:02d}".format(*time)

def _formatDate(date: tuple) -> str:
    return str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])


def _createDataFile(date: tuple):
    if not isAvailable(): return

    filename = _formatDate(date) + "-data.csv"

    print("createDataFile called: " + filename)
    file = open(LOG_DIR + "/" + filename, "a")
    template = open("template.csv", "r")

    print("Reading template: " + template.read())
    file.write('"Time","Moisture","Temperature","Humidity","Infrared","Watering?","BatteryLevel"')
    file.write("\n")
    file.close()
    
def _createInfoFile(date: tuple):
    if not isAvailable(): return

    filename = _formatDate(date) + "-info.csv"
    print("createInfoFile called: " + filename)
    file = open(LOG_DIR + "/" + filename, "w")
    file.close()


def isAvailable() -> bool:
    import sd
    return sd.isAvailable()