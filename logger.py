#!/usr/bin/env python
import serial
import datetime
import time
import psycopg2
from sense_hat import SenseHat
import password

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
sense = SenseHat()
sense.clear()

pressure = sense.get_pressure()
temp = sense.get_temperature()
humidity = sense.get_humidity()
	
while True:
	pressure = sense.get_pressure()
	temp = sense.get_temperature()
	humidity = sense.get_humidity()
        add_pressure(pressure,temp)
	add_humidity(humidity,temp)
	print("loopcount " + str(loopcount))
	loopcount += 1
	time.sleep(10.0)
