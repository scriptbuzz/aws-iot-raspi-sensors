# Name: M Bitar
# Project: Demo - Environmental Sensors Loggging
# Date: March 14, 2020
#
from sense_hat import SenseHat

from time import sleep
#sleep(1)
from random import randint
#num = randint(0,10)

sleep_val = .1
text_speed = .05
sense = SenseHat()
sense.clear()
r = 255
g = 255
b = 255

sense.clear((0, 0, 0))
red = (r,0,0)
back_clr = (0, 0, 0)
black = (0, 0, 0)
sense.show_message("AWS IoT Prototype", text_colour=red, back_colour=back_clr, scroll_speed=.05)


while (True):
    
    temp = sense.get_temperature()
    print("Temp: "+str(temp))
    sense.show_message("T:"+str(round(temp)), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sense.clear((0, 0, 0))
    sleep(sleep_val )
    
    pressure = sense.get_pressure()
    print("Pressure: "+str(round(pressure)))
    sense.show_message("P:"+str(round(pressure)), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sense.clear((0, 0, 0))
    sleep(sleep_val )
    
    humidity = sense.get_humidity()
    print("Humidity: "+str(round(humidity)))
    sense.show_message("H:"+str(round(humidity)), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sleep(sleep_val )
    
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    x=round(x, 2)
    y=round(y, 2)
    z=round(z, 2)
    print("x= {0}, y= {1}, z= {2}".format(x, y, z))
    sense.show_message("Z:"+str(z), text_colour=red, back_colour=back_clr, scroll_speed=text_speed)
    sleep(sleep_val )
    
    print("=" * 30)
    
    for event in sense.stick.get_events():
    # quit if button pressed
        sense.clear(0, 0, 0)
        quit()

