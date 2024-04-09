import uos
from lib import sdcard
import machine
import pins

def start(ignored=False, mountpoint = "/sd"):
    print("Starting SD Module...")

    try:
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
        uos.mount(vfs, mountpoint)
        print("Mount operation completed.")

        # Create a file and write something to it
        with open("/sd/hello.txt", "w") as file:
            file.write("Hello, SD World!\r\n")
            file.write("This is a test\r\n")

        # Open the file we just created and read from it
        with open("/sd/hello.txt", "r") as file:
            data = file.read()
            print("Hello message: ", data)

        return vfs
    except Exception as e:
        print("SD Card reading process encountered an exception...")
        print(e)
        

