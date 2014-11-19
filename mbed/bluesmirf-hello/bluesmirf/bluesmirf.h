#ifndef _BLUESMIRF_H_
#define _BLUESMIRF_H_

#include "mbed.h"

class Bluesmirf : public Serial {        
  public:
    Bluesmirf(PinName tx, PinName rx);
};

#endif