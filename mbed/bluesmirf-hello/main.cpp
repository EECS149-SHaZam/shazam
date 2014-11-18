#include "mbed.h"
#include "bluesmirf.h"

#define BT_TX PTC4
#define BT_RX PTC3

DigitalOut myled(LED_RED);
Serial pc(USBTX, USBRX);
Bluesmirf bt(BT_TX, BT_RX);

void init() {
}

void startup() {
    pc.printf("Hello World!\r\n");
    pc.printf("Bluesmirf 0x%x(0x%x) is on tx=0x%x and rx=0x%x\r\n", 
        &bt, sizeof(bt), BT_TX, BT_RX);
}

int main()
{
    init();
    startup();
    
    char c;
    while (true) {
        if (bt.readable()) {
            c = bt.getc();
            if (c == '\n') {
                pc.putc('\r');
                pc.putc('\n');
            } else {
                pc.putc(c);
            }
            myled = !myled;
        }
        if (pc.readable()) {
            c = pc.getc();
            if (c == '\r') {
//                bt.putc('\r');
                bt.putc('\n');
                pc.putc('\r');
                pc.putc('\n');
            } else { 
                bt.putc(c);
                pc.putc(c);
            }
            myled = !myled;
        }
    }
}
