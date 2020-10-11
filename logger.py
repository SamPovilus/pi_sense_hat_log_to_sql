#!/usr/bin/env python
import serial
import datetime
import time
from sense_hat import SenseHat
import password
from influxdb import InfluxDBClient
from datetime import datetime


loopcount = 0

client = InfluxDBClient("nas2",8086,"admin","test","climate")


sense = SenseHat()
sense.clear()

pressure = sense.get_pressure()
temp = sense.get_temperature()
humidity = sense.get_humidity()
	
brightness =50
while True:
        pressure = sense.get_pressure()
        temp = 9.0/5.0 * sense.get_temperature() + 32.0
        humidity = sense.get_humidity()
        print("loopcount " + str(loopcount))
        loopcount += 1
        sense.show_message("P:" + "{:0.2f}".format(pressure),text_colour=(0,brightness,brightness),back_colour=(0,0,0))
        sense.show_message("H:" + "{:0.2f}".format(humidity),text_colour=(brightness,0,0),back_colour=(0,0,0))
        sense.show_message("T:" + "{:0.2f}".format(temp),text_colour=(0,brightness,0),back_colour=(0,0,0))
        client.write_points([{"measurement":"climate","tags":{"host":"sense_hat"},"fields":{'pressure': pressure,'humidity':humidity,'tempurature':temp},"time":datetime.utcnow()}],time_precision='s',database='climate')
