from wiimote import Wiimote

# Does not seem to work with the leds, despite connecting.
# I can't stop the 4 leds from blinking together, like during
# initial discovery. This synchronous blinking masks the counting.

if __name__ == "__main__":
    wm = Wiimote()
    for i in xrange(60):
        print(i)
        wm.led_counter()


