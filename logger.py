#!/usr/bin/env python
import serial
import datetime
import time
import psycopg2
from sense_hat import SenseHat
import password
from influxdb import InfluxDBClient
from datetime import datetime


def add_humidity(humidity, temp):
                query = """                                                                            
    INSERT INTO                                                                                 
        humidity_display_humidity (humidity,temp,log_date,hostname)                                                                          
    VALUES                                                                                     
        (%s, %s, %s, %s)                                                                           
    """
                values = (humidity, temp, "now", "pib20")
                cur.execute(query, values)
                conn.commit()

def add_pressure(pressure, temp):
                query = """                                                                            
    INSERT INTO                                                                                
        humidity_display_pressure (pressure,temp,log_date,hostname)                                     
    VALUES                                                                                     
        (%s, %s, %s, %s)                                                                           
    """
                values = (pressure, temp, "now", "pib20")
                cur.execute(query, values)
                conn.commit()

                
conn = psycopg2.connect('host=pib1 user=pi password=' + password.get_password() + ' dbname=humidity_django_db')
cur = conn.cursor()
loopcount = 0

client = InfluxDBClient("nas2",8086,"climate")


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
	if(loopcount %(6) == 0):
		add_pressure(pressure,temp)
		add_humidity(humidity,temp)
	sense.show_message("P:" + "{:0.2f}".format(pressure),text_colour=(0,brightness,brightness),back_colour=(0,0,0))
	sense.show_message("H:" + "{:0.2f}".format(humidity),text_colour=(brightness,0,0),back_colour=(0,0,0))
	sense.show_message("T:" + "{:0.2f}".format(temp),text_colour=(0,brightness,0),back_colour=(0,0,0))
        client.write_points([{"measurement":"climate","tags":{"host":"sense_hat"},"fields":{'pressure': pressure,'humidity':humidity,'tempurature':temp},"time":datetime.now()}],time_precision='s',database='climate')
