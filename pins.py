from machine import Pin, ADC, SPI
from lib import sdcard
import uos
import dht

# DHT22
DHT_O = Pin(0, Pin.OUT)
DHT_DATA = Pin(1, Pin.IN)
SENSOR_DHT = dht.DHT22(DHT_DATA)

# PIR
# PIR_O = Pin(11, Pin.OUT)
PIR_DATA = Pin(9, Pin.IN)

# Pico onboard temperature
THERM_DATA = ADC(4)

# Moisture
MOIST_O = Pin(26, Pin.OUT)
MOIST_DATA = ADC(Pin(27))

# Relay module
RELAY_SIGNAL = Pin(2, Pin.OUT)

# SD Card module
SD_CS = Pin(17, Pin.OUT)
SD_SCK = Pin(18)
SD_TX = Pin(19)
SD_RX = Pin(16)

# Battery Voltage Reading
BATT_I = ADC(Pin(28))

_moisture_feed = []

def solveOnboardTemp():
    return 27 - THERM_DATA.read_u16() * 3.3 / 65535

def solveBatteryLevel() -> float:
    # Resistor 1 is 3.3K, Resistor 2 is 1K
    # This means the output voltage would be 7.4V * 0.2325 = 1.725V
    DIVIDER = const(1 / 4.3)
    MIN18650 = const(3.2)
    MAX18650 = const(4.2)

    voltage_read = (BATT_I.read_u16() / 65535) * 3.3
    real_voltage = voltage_read / DIVIDER
    percentage = (real_voltage - (MIN18650 * 2)) / ((MAX18650 - MIN18650) * 2)
    return percentage

def setRelayState(state: bool):
    if state:
        print("Relay on")
        RELAY_SIGNAL.low()
    else:
        print("Relay off")
        RELAY_SIGNAL.high()

def addMoistureReading(reading: float) -> float:
    _moisture_feed.append(reading)
    if len(_moisture_feed) > 5:
        _moisture_feed.pop(0)

    return getMoistureAverage()
    
def getMoistureAverage() -> float:
    return sum(_moisture_feed) / len(_moisture_feed)

async def allOn():
    print("Powering on all pins")
    DHT_O.high()
    # PIR_O.high()
    MOIST_O.high()
    setRelayState(False)

async def allOff():
    print("Powering off all pins")
    DHT_O.low()
    # PIR_O.low()
    setRelayState(False)
    MOIST_O.low()
