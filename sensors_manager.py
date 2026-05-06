import time
import pins
import asyncio
import cfg
import logger
import time_manager
import machine

class LiveData():
    def __init__(self, 
                 humidity: float=0, 
                 temperature: float=0,
                 moisture: float=0,
                 infrared: bool=False, 
                 battery: float=0,
                 extra: dict={}) -> None:
        
        self.humidity = humidity
        self.temperature = temperature
        self.moisture = moisture
        self.infrared = infrared
        self.battery = battery
        self.extra_data = extra

    def __str__(self) -> str:
        return f"humidity: {self.humidity}, temperature: {self.temperature}, moisture: {self.moisture}, infrared: {self.infrared}, battery: {self.battery}"

class SensorLoopManager():
    def __init__(self, debugDoNotLoop: bool=False) -> None:
        self.loop_current = asyncio.create_task(self.iterate())
        self.last_result = None
        self.stop_loop = False
        self.water_allowed = True
        self.last_watered = None
        
        if not debugDoNotLoop:
            asyncio.create_task(self.startLoop())

    # This function runs in a loop at an interval depending on the user's configuration (10 seconds by default)
    async def iterate(self) -> LiveData:
        try:
            live_humidty, live_temp, moisture = None, None, None

            try:
                ### Read the signals coming from the DHT22
                ### This would return its measured humidity and temperature
                pins.SENSOR_DHT.measure()
                live_humidty = pins.SENSOR_DHT.humidity()
                live_temp = pins.SENSOR_DHT.temperature()

            except OSError as e:
                ### At times it is unable to read the sensor, usually because it has recently powered on.
                ### In that case, another attempt will be made in the next iteration.
                print("Error fetching DHT22")

            except Exception as e:
                print(e)
                await asyncio.sleep(3)
            
            

            ### Read the moisture sensor by calling the function read_moisture().
            ### This function translates the signal coming from the moisture sensor.
            moisture_raw = read_moisture()
            moisture = pins.addMoistureReading(moisture_raw)

            ### Check if the condition is met to start watering
            ### The if-then statement is executed if moisture level is below the threshold (40% by default)
            if moisture < cfg.get("water_threshold") and self.water_allowed:

                ### The water() function is called.
                ### The function tells the relay to switch on which starts powering the water pump.
                asyncio.create_task(self.water())

                ### A pause period is also inititated that disables watering for ten minutes.
                ### This pause period disables watering despite when the conditions are met.
                asyncio.create_task(self.pausePeriod())

            ### Prepares data to be sent.
            data = LiveData(
                humidity=live_humidty or 0, 
                temperature=live_temp or 0, 
                moisture=moisture or 0, 
                infrared=read_pir() or False,
                battery=pins.solveBatteryLevel() or 0,
                extra={"moisture_raw": moisture_raw, "last_watered": self.last_watered}
            )
            
            ### Send the result for other modules to see.
            ### For example, the web app uses this data to display to the user.
            self.last_result = data

            ### Send the data to the logger.
            ### The logger writes the data into a file inside the installed SD Card.
            logger.logData(data)
            return data
        except Exception as e:

            ### If an error is encountered, it is sent to the logger.
            print("Loop iteration encountered an error: " + str(e))
            logger.logInfo("ERROR", "Loop iteration encountered an error: " + str(e))
            return LiveData()
    
    async def water(self):
        print("Watering!")
        now = time_manager.getRealLocaltime()
        self.last_watered = logger._formatDate(now) + " " + logger._formatTime(now)
        logger.logInfo("INFO", "Watering for {} seconds".format(cfg.get("water_time")))
        pins.setRelayState(True)
        await asyncio.sleep(cfg.get("water_time"))
        logger.logInfo("INFO", "Watering finished")
        pins.setRelayState(False)

    async def waterManual(self, duration: int):
        logger.logInfo("INFO", "Watering for {} seconds".format(duration))
        pins.setRelayState(True)
        await asyncio.sleep(duration)
        logger.logInfo("INFO", "Watering finished")
        pins.setRelayState(False)

    async def pausePeriod(self):
        self.water_allowed = False
        await asyncio.sleep(cfg.get("water_pause"))
        self.water_allowed = True
        print("Pause period has ended.")
        logger.logInfo("INFO", "Pause period has ended")
    
    def stop(self):
        self.stop_loop = True

    async def startLoop(self):
        while not self.stop_loop:
            await self.loop_current
            self.loop_current = asyncio.create_task(self.iterate())
            await asyncio.sleep(cfg.get("check_interval"))
        print("Sensor loop has stopped!")
    
    def waitForFinish(self) -> None:
        async def wait():
            await self.loop_current
            return
        asyncio.run(wait())
        return

def read_moisture() -> float:
    return 1 - (pins.MOIST_DATA.read_u16() / 65535)

def read_pir() -> bool:
    res = pins.PIR_DATA.value()
    if res == 1:
        return True
    else:
        return False