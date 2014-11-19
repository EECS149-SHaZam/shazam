#include "mbed.h"
#define LF      "\n"
#define CRLF    "\r\n"
#define NL      CRLF

DigitalOut myled(LED_GREEN);
Serial pc(USBTX, USBRX);


int main()
{
    int i = 0;
    pc.printf("Hello World!" NL);

    while (true) {
        wait(0.5f); // wait a small period of time
        pc.printf("%d" NL, i); // print the value of variable i
        i++; // increment the variable
        myled = !myled; // toggle a led
    }
}
