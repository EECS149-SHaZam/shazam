import cwiid
import time
from sys import stdout

def write(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def connect(tries=10):
    print("To stop this program, press ctrl-c.")
    print("Press 1 and 2 on the Wiimote now.")
    print("Connecting to the Wiimote")
    
    wm = None
    for i in xrange(tries):
        write('.')
        try:
            wm = cwiid.Wiimote()
            print("Success!")
            return wm
        except:
            pass
    print("Tried %d times and failed to connect.")
    

