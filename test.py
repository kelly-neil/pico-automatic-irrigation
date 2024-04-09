from machine import Pin, ADC
import dht
import time

# Built-in LED
pin = Pin("LED", Pin.OUT)

# DHT22
dht_o = Pin(15, Pin.OUT)
dht_sensor = dht.DHT22(Pin(14))

# PicoThermometer
picoth = ADC(4)

# PIR Motion Sensor
pir_o = Pin(11, Pin.OUT)
pir_sensor = Pin(10, Pin.IN)

# Soil moisture sensor
soil_o = Pin(2, Pin.OUT)
soil_sensor = ADC(Pin(26))

def solveOnboardTemp(v):
    return 27 - (v - 0.706)/0.001721

print("LED starts flashing...")
#dht_o.high()
#pir_o.high()
soil_o.high()
while True:
    try:
        #pin.toggle()
        #dht_sensor.measure()
        #picoth_i = picoth.read_u16() * 3.3 / 65535
        #print("DHT22: ",dht_sensor.temperature(), dht_sensor.humidity())
        #print("Integrated: ", solveOnboardTemp(picoth_i))
        #print("PIR: ", pir_sensor.value())
        print("Soil: ", soil_sensor.read_u16() * 3.3 / 65535)
        print("(by percent): ", soil_sensor.read_u16() / 65535)
        time.sleep(3) # sleep 1sec
    except KeyboardInterrupt:
        break
    except OSError as e:
        print(e)
        time.sleep(2)
pin.off()
print("Finished.")