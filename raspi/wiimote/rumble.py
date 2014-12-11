from wiimote import connect
from utils import write

import cwiid
import time

if __name__ == "__main__":
    wm = connect()
    print('Rumbling...')
    for i in xrange(100):
        write('\r%d  ' % i)
        if i % 3:
            wm.rumble = False
        else:
            wm.rumble = True
        time.sleep(0.5)
    print("")
    wm.rumble = False


