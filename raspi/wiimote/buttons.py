class Buttons(object):
    def __init__(self, wm):
        self.a = False
        self.b = False
        
        if not wm:
            return
        
        buttons = wm.state['buttons']
        
        if not buttons:
            return
        
        self.a = bool(buttons & 0x8)
        self.b = bool(buttons & 0x4)
        self.left = bool(buttons & 0x10)
        self.right = bool(buttons & 0x20)
        self.down = bool(buttons & 0x40)
        self.up = bool(buttons & 0x80)
    
    
