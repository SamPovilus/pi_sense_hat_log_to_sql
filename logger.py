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
        
hostname = getHostname()
while True:
        load = getLoad()
        print(load)
        print(hostname)
        loopcount += 1
        #client.write_points([{"measurement":"climate","tags":{"host":hostname},"fields":{'pressure': pressure,'humidity':humidity,'tempurature':temp},"time":datetime.utcnow()}],time_precision='s',database='climate')
