import json
import pins
import sensors_manager

def JSON(duration, start, average_by):
    output = {
        "record_time":{
            "time_start":None,
            "time_end":None,
            "duration":None   
        },
        "sensors": {
            "moisture":None,
            "temperature":None,
            "humidity":None,
            "infrared":None
        },
        "active": {
            "moisture":None,
            "temperature":None,
            "humidity":None,
            "infrared":None
        }
    }
    return None

def format_livedata(data: sensors_manager.LiveData | None) -> str:
    output = {
        "record_time":{
            "time":None,
        },
        "sensors": {

        },
        "active": {

        }
    }

    # set the values in keys accordingly

    if data == None:
        return json.dumps(output)
    
    sensors = output["sensors"]
    sensors["moisture"] = data.moisture
    sensors["temperature"] = data.temperature
    sensors["humidity"] = data.humidity
    sensors["infrared"] = data.infrared
    sensors["battery"] = data.battery

    return json.dumps(output)