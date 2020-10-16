#!/usr/bin/env python
import datetime
import time
from influxdb import InfluxDBClient
from datetime import datetime
import subprocess

loopcount = 0

client = InfluxDBClient("nas2",8086,"admin","test","climate")

def getLoad():
        f = open("/proc/loadavg", "r")
        load = f.readline().strip().split()[1]
        f.close()
        return (load)
        
def getHostname():
        result = subprocess.run(['hostname'], stdout=subprocess.PIPE)
        return (result.stdout.decode().strip())

def getMemory():
        f = open("/proc/meminfo", "r")
        memDict = {}
        for line in f:
                memDict[line.strip().split()[0]] = line.strip().split()[1]
        f.close()
        #print(memDict)
        memUsedPercent = (1.0-(int(memDict["MemFree:"])/int(memDict["MemTotal:"])))
        try:
                swapUsedPercent = (1.0-(int(memDict["SwapFree:"])/int(memDict["SwapTotal:"])))
        except ZeroDivisionError:
                swapUsedPercent = -1.0
        
        return [memUsedPercent,swapUsedPercent]

import os
def getThermalZones():
        for zone in os.listdir("/sys/class/thermal/"):
                if "thermal_zone" in zone:
                        f = open("/sys/class/thermal/" + zone + "/temp")
                        print(f.readline().strip())
                        f.close()
        
hostname = getHostname()
while True:
        load = getLoad()
        mem = getMemory()
        print(load)
        print(hostname)
        print(mem)
        getThermalZones()
        loopcount += 1
        #client.write_points([{"measurement":"climate","tags":{"host":hostname},"fields":{'pressure': pressure,'humidity':humidity,'tempurature':temp},"time":datetime.utcnow()}],time_precision='s',database='climate')
