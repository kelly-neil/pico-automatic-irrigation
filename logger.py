import sensors_manager
import time_manager
import os

# logger.py logs data according to the current day.
# If the day changes, a new file will be created.
# Logs are saved on a folder named /sd/log:
# 2 logs are created for each day, namely:
# YYYY-MM-DD-data.csv: logs sensor data that is monitored in intervals. 
# YYYY-MM-DD-info.csv: logs descriptive information, including watering, errors, and other important information.

LOG_DIR = const("/sd/log/")

def now() -> tuple:
    return time_manager.getRealLocaltime()

def logData(data: sensors_manager.LiveData):
    # CSV format is the following:
    # "Time","Moisture","Temperature","Humidity","Infrared","Watering?","BatteryLevel"
    out = ""
    out += formatTime(now()) + ","

    out += str(data.moisture) + ","
    out += str(data.temperature) + ","
    out += str(data.humidity) + ","
    out += str(data.infrared) + ","
    out += str("n/a") + ","
    out += str(data.battery)

    nametarget = LOG_DIR + formatDate(now()) + "-data.csv"

    print("logData called: " + nametarget)
    print("Output: " + out)

    try:
        os.stat(nametarget)
    except OSError:
        createDataFile(now())
        logInfo("INFO", "Created data file")

    file = open(nametarget, "a")
    file.write(out)
    file.write("\n")
    file.close()

def logInfo(tag: str, msg: str):
    out = ""
    out += "[{}] ".format(formatTime(now()))
    out += " {} - ".format(tag)
    out += msg

    nametarget = LOG_DIR + formatDate(now()) + "-info.csv"
    print("logInfo called: " + nametarget)

    try:
        os.stat(nametarget)
    except OSError:
        createInfoFile(now())
        logInfo("INFO", "Created info file")

    file = open(nametarget, "a")
    file.write(out)
    file.write("\n")
    file.close()

def formatTime(time: tuple) -> str:
    return "{3:02d}:{4:02d}:{5:02d}".format(*time)

def formatDate(date: tuple) -> str:
    return str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])


def createDataFile(date: tuple):
    filename = formatDate(date) + "-data.csv"

    print("createDataFile called: " + filename)
    file = open(LOG_DIR + filename, "a")
    template = open("template.csv", "r")

    print("Reading template: " + template.read())
    file.write('"Time","Moisture","Temperature","Humidity","Infrared","Watering?","BatteryLevel"')
    file.write("\n")
    file.close()
    
def createInfoFile(date: tuple):
    filename = formatDate(date) + "-info.csv"
    print("createInfoFile called: " + filename)
    file = open(LOG_DIR + filename, "w")
    file.close()

def start():
    print("Starting Logger Module")

    try:
        os.stat("/sd/log")
    except OSError:
        print("Log directory probably doesn't exist, creating it.")
        os.chdir("sd")
        os.mkdir("log")
        os.chdir("/")
    logInfo("INFO", "Logging is ready")