import uos
from lib import sdcard
import machine
import pins

MOUNT_POINT = const("/sd")

def start(ignored=False):
    try:
        print("Starting SD Module...")

        SD_SPI = machine.SPI(0,
            baudrate=1000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=machine.SPI.MSB,
            sck=pins.SD_SCK,
            mosi=pins.SD_TX,
            miso=pins.SD_RX)
        
        SD_CARD = sdcard.SDCard(SD_SPI, pins.SD_CS)
        vfs = uos.VfsFat(SD_CARD)
        uos.mount(vfs, MOUNT_POINT)
        print("Mount operation completed.")

        import random
        random = random.getrandbits(32).to_bytes(4, "little")

        # Check if writing and reading works
        with open(MOUNT_POINT + "/test", "wb") as file:
            file.write(random)

        with open(MOUNT_POINT + "/test", "rb") as file:
            data = file.read()

        if data != random:
            raise Exception("File readback does not match!")
        else:
            print("Write and read was OK")

        return vfs
    except Exception as e:
        if ignored:
            print("Ignored module caught an error: ", e)
        else:
            raise e

def isAvailable() -> bool:
    from lib import files
    return files.dirExists(MOUNT_POINT)