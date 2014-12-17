from wiimote import connect
import time
import cwiid
from utils import write 


# Does not seem to work with the leds, despite connecting.
# I can't stop the 4 leds from blinking together, like during
# initial discovery. This synchronous blinking masks the counting.

if __name__ == "__main__":
    wm = connect()
    time.sleep(1)
    
    print("Counting...")
    for i in xrange(100):
        hx = i % 16
        write('\r' + str(hx) + ' ')
        wm.led = hx
        time.sleep(0.5)
    print("")

