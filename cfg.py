import json
import os
import sd

cfg = {}
default_cfg = {}
available = False
_config_path = sd.MOUNT_POINT + "/config.json"

def start(ignored = False):
    global cfg, default_cfg, available

    try:

        with open("default.json", "r") as dfile:
            default_cfg = json.loads(dfile.read())

        if not sd.isAvailable():
            raise ValueError("SD card not available")

        try:
            with open(_config_path, "r") as file:
                try:
                    cfg = json.loads(file.read())
                except ValueError:
                    print("Config JSON was malformed!")
                    file.close()
                    cfg = setDefault()
        except OSError:
            cfg = setDefault()

        available = True
    except Exception as e:
        if ignored:
            print("Ignored module caught an error: ", e)
        else:
            raise e

def setDefault():
    print("Setting default config was called")
    with open(_config_path, "w") as file:
        with open("default.json", "r") as default:
            read = default.read()
            file.write(read)
            print("Applying default: ", read)
            result = json.loads(read)
            return result

def update(new_json):
    if not isAvailable(): return

    global cfg
    try:
        cfg = json.loads(new_json)
    except ValueError:
        print("Config JSON was malformed!")
        raise ValueError("Malformed JSON")
    with open(_config_path, "w") as file:
        file.write(new_json)

def get(field):
    # If not in cfg, get default.
    return cfg.get(field, default_cfg.get(field))

def has(field):
    return field in cfg

def set(field, value):
    cfg[field] = value

def save():
    if not isAvailable(): return

    with open(_config_path, "w") as file:
        file.write(json.dumps(cfg))
        file.close()

def isAvailable():
    available_sd = sd.isAvailable()
    return available_sd and available 