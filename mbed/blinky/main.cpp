#include "mbed.h"

DigitalOut rled(LED1);
DigitalOut gled(LED2);
DigitalOut bled(LED3);

int main() {
    rled = 1; // turn off the red LED
    gled = 1; // green off
    while(1) {
        bled = 1; // blue off
        wait(0.2);
        bled = 0; // blue on
        wait(0.2);
    }
}
