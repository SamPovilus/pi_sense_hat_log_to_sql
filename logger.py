#!/usr/bin/env python
import serial
import datetime
import time
import psycopg2
from sense_hat import SenseHat

def add_humidity(humidity, temp):
                query = """                                                                            
    INSERT INTO                                                                                
        humidity_display_humidity (humidity,temp,log_date)                                                                          
    VALUES                                                                                     
        (%s, %s, %s)                                                                           
    """
                values = ("now",humidity, temp)
                cur.execute(query, values)
                conn.commit()

def add_pressure(pressure, temp):
                query = """                                                                            
    INSERT INTO                                                                                
        humidity_display_pressure (pressure,temp,log_date)                                     
    VALUES                                                                                     
        (%s, %s, %s)                                                                           
    """
                values = ("now",pressure, temp)
                cur.execute(query, values)
                conn.commit()

                
conn = psycopg2.connect('host=pib1 user=pi password=<redacted> dbname=humidity_django_db')
cur = conn.cursor()
loopcount = 0
sense = SenseHat()
sense.clear()

pressure = sense.get_pressure()
temp = sense.get_tempurature()
humidity = sense.get_humidity()
	
while True:
	pressure = sense.get_pressure()
	temp = sense.get_tempurature()
	humidity = sense.get_humidity()
        add_pressure(pressure,temp)
	add_humidity(humidity,temp)
	loopcount += 1
	
