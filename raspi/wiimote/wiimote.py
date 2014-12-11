import cwiid
import time
from utils import write


def connect(tries=10):
    print("To stop this program, press ctrl-c.")
    print("Press 1 and 2 on the Wiimote now.")
    write("Connecting to the Wiimote")
    
    wm = None
    for i in xrange(tries):
        write('.')
        try:
            wm = cwiid.Wiimote()
            print("\nSuccess!")
            return wm
        except:
            pass
    print("Tried %d times and failed to connect." % tries)

