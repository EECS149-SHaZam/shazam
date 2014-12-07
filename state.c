typedef enum {
    OFF,
    ON,
    PITCH_STAY,
    PITCH_TRACK,
    YAW_STAY
    YAW_TRACK,

} state_t;

struct data{
    int isOn;
    int yawAngle;
    int pitchAngle;
};

void perform_calibration(){
    //Perform any calibration we need
}

void perform_transition(state_t prev, state_t curr){
    if (prev == OFF && curr == ON){
        state_t = ON;
        perform_calibration();
    }
    if (state_t == PITCH_STAY){
        //stop moving about the Z axis
    }
    if (state_t == YAW_STAY){
        //stop moving about the Y axis
    }
    if (state_t == PITCH_TRACK){
        //move accordingly
    }
    if (state_t == YAW_TRACK){
        //move accordingly
    }
    if (state_t == OFF){
        //stop all movement and wait for ON state before resuming
    }
}

void get_data(){
    //Returns struct data with all the info we need to judge which state to move our robot in
    //and the appropriate thresholds.
}

void start(){
    prev_state = state_t;
    results = get_data();
    if (results->isOn){
        curr_state = ON;
    }
    if (results->isOn == 0){
        curr_state = OFF;
    }
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
    perform_transition(prev_state, curr_state);
}

int main(){
    state_t = OFF;
    while(1){
        start();
    }
}