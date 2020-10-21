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
import re
def getThermalZones():
        thermalValues = []
        for zone in os.listdir("/sys/class/thermal/"):
                if "thermal_zone" in zone:
                        f = open("/sys/class/thermal/" + zone + "/temp")
                        thermalValues.append({int(re.findall(r'\d+',zone)[0]),int(f.readline().strip())})
                        f.close()
        return thermalValues

def getSensors():
        result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
        result = result.stdout.splitlines()
        lineNum = 0
        while lineNum < len(result):
                device = result[lineNum]
                lineNum += 2
                while len(result[lineNum]) > 1:
                        sensor = str(result[lineNum]).split(":")[0]
                        reading =  str(result[lineNum]).split(":")[1].split()[0]
                        if(reading[-1] == 'C'):
                                print("got a temp")
                                reading = float(str(re.findall("\d+\.\d+",reading)[0]))
                        elif(str(result[lineNum]).split(":")[1].split()[1][0:3] == "RPM"):
                                print("got a fan speed")
                                reading = int(reading)
                        else:
                                print("not sure " + str(result[lineNum]).split(":")[1].split()[1])
                                lineNum+= 1
                        print("device: " + str(device) + " sensor: " + str(sensor) + " reading: " + str(str(reading)))
                        lineNum += 1
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
        #client.write_points([{"measurement":"climate","tags":{"host":hostname},"fields":{'pressure': pressure,'humidity':humidity,'tempurature':temp},"time":datetime.utcnow()}],time_precision='s',database='climate')
