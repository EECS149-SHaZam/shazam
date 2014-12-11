from wiimote import Wiimote


if __name__ == "__main__":
    wm = Wiimote()
    for i in xrange(60):
        wm.rumble_pulse()

