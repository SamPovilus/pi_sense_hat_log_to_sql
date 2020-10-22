#!/usr/bin/env python3
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
        return ({"load_average":float(load)})
        
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
        
        return {"mem_used":memUsedPercent,"swap_used":swapUsedPercent}

import os
import re
def getThermalZones():
        thermalValues = {}
        for zone in os.listdir("/sys/class/thermal/"):
                if "thermal_zone" in zone:
                        f = open("/sys/class/thermal/" + zone + "/temp")
                        thermalValues[zone] = (int(f.readline().strip()))
                        f.close()
        return thermalValues

def getSensors():
        try:
                result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
        except FileNotFoundError:
                return {}
        result = result.stdout.splitlines()
        lineNum = 0
        retVal = {}
        while lineNum < len(result):
                device = result[lineNum]
                lineNum += 2
                while len(result[lineNum]) > 1:
                        match = re.match("^([^:]+):\s*\+*(\d+.\d+)[\s°]([a-zA-Z]+)",(result[lineNum]).decode("utf-8"))
                        lineNum += 1
                        retVal[device + match.group(1) + "(" + match.group(3) + ")"] = match.group(2)
                        #print("Sensor: " + match.group(1) + " Value: " + match.group(2))
                lineNum += 1
        

hostname = getHostname()
while True:
        load = getLoad()
        mem = getMemory()
        print(load)
        print(hostname)
        print(mem)
        thermalZones = getThermalZones()
        print(thermalZones)
        getSensors()
        loopcount += 1
        #client.write_points([{"measurement":"computer_status","tags":{"host":hostname},"fields":{'pressure': pressure,'humidity':humidity,'tempurature':temp},"time":datetime.utcnow()}],time_precision='s',database='climate')
