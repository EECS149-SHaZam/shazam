#define ID				    (2)
#define LENGTH				(3)
#define INSTRUCTION			(4)
#define PARAMETER			(5)
#define DEFAULT_BAUDNUMBER	(1)

P_ID = 3;
P_LED_CONTROL = 25;
P_PRESENT_POSITION = 36; // LSB of present position
P_GOAL_POSITION = 30;
P_TORQUE_ENABLE = 24;
P_MOVING_SPEED = 32;
P_BAUD_RATE = 4;
P_PRESENT_VOLTAGE = 42;
P_MOVING = 46;
P_CW_ANGLE_LIMIT = 6;

MIN_PITCH = 203;
MAX_PITCH = 828;
DOWN_PITCH = 515;

STRAIGHT_YAW = 362;
MIN_YAW = 50; // -90deg, left turn
MAX_YAW = 664; // +90deg, right turn

yawId = 2;
pitchId = 3;
broadcastId = 254; % Broad cast ID

//%%%%%%% CODE %%%%%
    // Turning on LED and motor is one byte, so packet length is 4.
    // If writing motor position, this is two bytes, so packet length is 5.
gbInstructionPacket[ID] = (unsigned char)id;                // motor ID
gbInstructionPacket[INSTRUCTION] = INST_WRITE;
gbInstructionPacket[PARAMETER] = (unsigned char)address;    // variable to write to
gbInstructionPacket[PARAMETER+1] = (unsigned char)value;    // value to write
gbInstructionPacket[LENGTH] = 4;

// checksumming
gbInstructionPacket[0] = 0xff;
	gbInstructionPacket[1] = 0xff;
	for( i=0; i<(gbInstructionPacket[LENGTH]+1); i++ )
		checksum += gbInstructionPacket[i+2];
	gbInstructionPacket[gbInstructionPacket[LENGTH]+3] = ~checksum;
// END checksumming

    // Length of message
TxNumByte = gbInstructionPacket[LENGTH] + 4;
	RealTxNumByte = dxl_hal_tx( (unsigned char*)gbInstructionPacket, TxNumByte );

    // actually send the message
int dxl_hal_tx( unsigned char *pPacket, int numPacket )
{
	// Transmiting date
	// *pPacket: data array pointer
	// numPacket: number of data array
	// Return: number of data transmitted. -1 is error.
	DWORD dwToWrite, dwWritten;

	dwToWrite = (DWORD)numPacket;
	dwWritten = 0;

	if( WriteFile( ghSerial_Handle, pPacket, dwToWrite, &dwWritten, NULL ) == FALSE )
		return -1;
	
	return (int)dwWritten;
}