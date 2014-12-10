typedef enum {
    OFF,
    ON,
    PITCH_STAY,
    PITCH_TRACK,
    YAW_STAY
    YAW_TRACK,

} state_t;

typedef struct data{
    int yawAngle;
    int pitchAngle;
};

int netAngle = 0;


void perform_calibration(){
    //Perform any calibration we need
}


void get_data(){
    //Returns struct data with all the info we need to judge which state to move our robot in
    //and the appropriate thresholds.
}

void stateChart(){
    static state_t state;
    /*
        state transitions
    */
    results = get_data();
    if (results->yawAngle >= threshold){
        curr_state = YAW_TRACK;
    }
    if (results->yawAngle < threshold){
        curr_state = YAW_STAY;
    }
    if (results->pitchAngle >= threshold){
        curr_state = PITCH_TRACK;
    }
    if (results->pitchAngle < threshold){
        curr_state = PITCH_STAY;
    }

    /*
        state actions
    */
    if (state == PITCH_STAY){
        //stop moving about the Z axis
    }
    if (state == YAW_STAY){
        //stop moving about the Y axis
    }
    if (state == PITCH_TRACK){
        //move accordingly
    }
    if (state == YAW_TRACK){
        //move accordingly
    }
    if (state == OFF){
        //stop all movement and wait for ON state before resuming
    }

    
}

int main(){
    perform_calibration();
    while(1){
        start();
    }
}
