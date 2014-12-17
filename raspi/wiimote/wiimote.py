from time import sleep

from utils import write
import cwiid
from lights import Lights


def connect(tries=10, verbose=True, fail_callback=None):
    if verbose:
        print("Press 1 and 2 on the Wiimote now.")
        print("Searching for Wiimote...")

    wm = None
    for i in xrange(tries):
        try:
            wm = cwiid.Wiimote()
            break
        except:
            if fail_callback: fail_callback()
    if wm:
        if verbose: print("  Found!")
        success_lights(wm)
        return wm
    else:
        if verbose: print("Tried %d times and failed to connect." % tries)


def connect_loop(verbose=True, fail_callback=None):
    if verbose:
        print("Searching for Wiimote...")
    wm = None
    while not wm:
        try:
            wm = cwiid.Wiimote()
        except:
            if fail_callback: fail_callback()
    if verbose: print("  Found!")
    success_lights(wm)
    return wm

def success_lights(wm):
    sleep(0.2)
    lights = Lights(wm).auto()
    sleep(2)

