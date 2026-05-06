import os

def fileExists(path):
    try:
        return (os.stat(path)[0] & 0x4000) == 0
    except OSError:
        return False
    
def dirExists(path):
    try:
        return (os.stat(path)[0] & 0x4000) != 0
    except OSError:
        return False
    
def exists(path):
    try:
        return os.stat(path)
    except OSError:
        return False