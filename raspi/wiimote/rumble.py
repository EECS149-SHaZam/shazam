from wiimote import connect

import cwiid
import time

if __name__ == "__main__":
    wm = connect()
    for i in xrange(100):
        print(i)
        if i % 3:
            self.wm.rumble = False
        else:
            self.wm.rumble = True
        time.sleep(0.5)
    self.wm.rumble = False


