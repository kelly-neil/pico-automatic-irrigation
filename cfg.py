import json
import os

cfg = {}
default_cfg = {}

def start(ignored = False):
    global cfg, default_cfg

    dfile = open("default.json", "r")
    default_cfg = json.loads(dfile.read())
    dfile.close()

    try:
        file = open("config.json", "r")
        try:
            cfg = json.loads(file.read())
        except ValueError:
            print("Config JSON was malformed!")
            cfg = setDefault()
        file.close()
    except OSError:
        cfg = setDefault()

def setDefault():
    print("Setting default config was called")
    file = open("config.json", "w")
    default = open("default.json", "r")
    file.write(default.read())
    print("Applying default: ", default.read())
    result = json.loads(default.read())
    file.close()
    default.close()
    return result

def update(new_json):
    global cfg
    try:
        cfg = json.loads(new_json)
    except ValueError:
        print("Config JSON was malformed!")
        raise ValueError("Malformed JSON")
    file = open("config.json", "w")
    file.write(new_json)
    file.close()

def get(field):
    # If not in cfg, get default.
    return cfg.get(field, default_cfg.get(field))

def has(field):
    return field in cfg

def set(field, value):
    cfg[field] = value

def save():
    file = open("config.json", "w")
    file.write(json.dumps(cfg))
    file.close()