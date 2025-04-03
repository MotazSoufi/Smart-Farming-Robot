from gpiozero import LED
import time

r = LED(21)

r.on()

time.sleep(1)

r.close()