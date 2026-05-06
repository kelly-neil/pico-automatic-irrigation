import machine
import time
import sensors_manager
import asyncio
import cfg
import sd
import logger

from machine import Pin
import os
import server_handler
import pins

### Choose which to ignore during startup. 

# Ignored modules do not throw errors and will not prevent the device from starting up.
IGNORE_SD = False # Requires IGNORE_CFG and IGNORE_LOGGER to be also True
IGNORE_CFG = False
IGNORE_LOGGER = False
IGNORE_WIFI = False

led = Pin("LED", Pin.OUT)
signal_stop = False
pins.setRelayState(False)

async def blink():
    count = 0
    while True:
        count += 1
        led.toggle()
        await asyncio.sleep(0.5)

async def blink_success():
    for i in range(5):
        led.off()
        await asyncio.sleep(0.1)
        led.on()
        await asyncio.sleep(0.1)

async def blink_alert():
    while True:
        led.on()
        await asyncio.sleep(0.05)
        led.off()
        await asyncio.sleep(0.45)

def onClose():
    led.off()
    asyncio.run(pins.allOff())
    print("Everything has stopped.")

async def main():
    global signal_stop

    ### Initialize pins
    asyncio.create_task(pins.allOn())
    led.high()

    ### Start essential modules
    sd.start(IGNORE_SD)
    cfg.start(IGNORE_CFG)

    ### Connect to wifi
    task_blink = asyncio.create_task(blink())
    try:
        wifi_found = False
        task_wifi = None
        if cfg.has("good_network"):
            print("Attempting to connect to good network first...")
            good_network = cfg.get("good_network")
            creds = cfg.get("wifi_creds")[good_network]
            task_wifi = await server_handler.wifi(creds[0], creds[1])
            if task_wifi != None:
                wifi_found = True
            else:
                print("Timeout.")
        else:
            print("No good network found. Trying all networks...")

        if not wifi_found:
            index = 0
            for creds in cfg.get("wifi_creds"):
                print("Attempting to connect: " + str(creds))
                task_wifi = await server_handler.wifi(creds[0], creds[1])
                if task_wifi != None:
                    wifi_found = True
                    break
                print("Timeout.")
                index += 1
        
            if not wifi_found:
                task_blink.cancel()
                print("Can't proceed! Not connected to a network!")
                await blink_alert()
                return
            else:
                print("Remembering this network as good network.")
                print("Index: ", index, ", Creds: ", cfg.get("wifi_creds")[index])
                
                cfg.set("good_network", index)
                cfg.save()
        else:
            print("Connected to good network...")

    except Exception as e:
        if IGNORE_WIFI:
            print("Ignored module caught an error: ", e)
        else:
            raise e

    ### Update time with an NTP
    if time.localtime()[0] == 2021:
        print("The clock is behind. Updating...")
        import time_manager
        task_ntp = await time_manager.set_time()
        if task_ntp:
            print("Time updated successfully.")
            print("The time is ", time_manager.getRealLocaltime(), ".")
        else:
            print("Couldn't do it! Aborting!!")
            await blink_alert()
            return

    # Logging enabled
    logger.start(IGNORE_LOGGER)
    logger.logInfo("INFO", "Pico IP is " + str(task_wifi))

    ### Initialize sensors
    task_blink.cancel()
    asyncio.create_task(blink_success())
    
    loop = sensors_manager.SensorLoopManager()

    # Create a stop function to be passed for the server to call whenever it wants to.
    # This may not work.
    def sendStopSignal():
        global signal_stop
        signal_stop = True

    machine.freq(64 * 1000000)

    ### Run the server
    master_stop = asyncio.create_task(server_handler.run(sendStopSignal, loop))

    ### Closing
    async def waitStopSignal(tostop):
        global signal_stop
        while not signal_stop:
            await asyncio.sleep(5)
        tostop.cancel()
        print("Signal received. Now stopping.")
        while not tostop.cancelled():
            await asyncio.sleep(1)
        print("Server should have nothing else to do")
    
    asyncio.create_task(waitStopSignal(master_stop))
    await master_stop
    onClose()


### Let's roll
try:
    asyncio.run(main())
except KeyboardInterrupt:
    onClose()