#include "bluesmirf.h"


Bluesmirf::Bluesmirf(PinName tx, PinName rx) : Serial(tx, rx) {
    baud(115200);
    printf("$$$");
    wait(0.1);
    printf("SS,SerialPort\n");
    wait(0.1);
    printf("U,9600,N\n");
    wait(0.1);
    baud(9600);
    printf("---\n");
    wait(0.1);
}
