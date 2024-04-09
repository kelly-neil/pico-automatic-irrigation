import network
import socket
import time
import struct
import machine


from machine import Pin

NTP_DELTA = 2208988800
host = "time.google.com"

led = Pin("LED", Pin.OUT)
wlan = network.WLAN

async def set_time():
    success = True
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(10)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    print(tm)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    return success

def getRealLocaltime(offset_h = 8, offset_m = 0):
    offsetted = getRealTime(offset_h, offset_m)
    return time.localtime(offsetted)

def getRealTime(offset_h = 8, offset_m = 0):
    return time.time() + offset_h * 3600 + offset_m * 60

def formatTime(time = getRealLocaltime()):
    return "{}:{}:{}".format(time[3], time[4], time[5])