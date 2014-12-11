import cwiid
import time

class Wiimote(object):
    def __init__(self):
        self.wm = cwiid.Wiimote()
        if self.wm:
            print("wm has been set! Value is:")
            print(str(self.wm))
        else:
            print("failed to create wm.")
            return 1

    def bin_led_counter(self, delay=0.5):
        for i in xrange(16):
            self.wm.led = i
            time.sleep(delay)
    
    def rumble_pulse(self, delay=0.5):
        for i in xrange(16):
            if i % 3:
                self.wm.rumble = False
            else:
                self.wm.rumble = True
            time.sleep(delay)
        self.wm.rumble = False
            
if __name__ == "__main__":
    wm = Wiimote()
    for i in xrange(60):
        wm.bin_led_counter()
        wm.rumble_pulse()
    
