from time import sleep
from wiimote import Lights, connect_loop
from rs485 import MotorController, enable_rts, disable_rts
import statechart


def blink_rts():
    disable_rts(False)
    sleep(0.5)
    enable_rts(False)


enable_rts()
wm = connect_loop(fail_callback=blink_rts)
mc = MotorController()
statechart.deploy(wm, mc)

