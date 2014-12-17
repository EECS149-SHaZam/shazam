class Lights(object):
    def __init__(self, wm):
        self._wm = wm

    def auto(self):
        self._wm.led = 0x9

    def manual(self):
        self._wm.led = 0x6

    def off(self):
        self._wm.led = 0

if __name__ == "__main__":
    import cwiid
    from time import sleep
    wm = cwiid.Wiimote()
    sleep(0.2)  # time to stop blinking from pairing
    Lights(wm).auto()
