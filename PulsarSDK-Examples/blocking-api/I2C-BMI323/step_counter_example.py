import time
from blockingpulsar import *
from BMI323 import BMI323
from BMI323_definitions import *
from ctypes import *

def main():
    device = BlockingPulsar()

    open_result = device.open()
    print("Open result: ", open_result)

    if open_result["opcode"] != 0:
        print("Failed to open device")
        exit(1)

    result = device.getDeviceInfo()
    print("Device info: ", result)

    # Set voltage
    result = device.setI2cSpiUartGpioVoltage(voltage_mV=3300)
    print("Set I2C Voltage result: ", result)

    # Initialize the I2C interface
    result = device.i2cControllerInit(
        frequency=1000000, 
        busId=I2cBus.I2C_BUS_A, 
        pullUpResistorsValue=I2cPullUpResistorsValue.I2C_PULLUP_2_2kOhm
    )
    print("I2C Controller Init result: ", result)

    sensor = BMI323(controller=device, bus_id=I2cBus.I2C_BUS_A)

    sensor.use_feature_step_counter = True

    sensor.init_device()
        
    sensor.calibrate()

    keep_running = True

    def on_key(event):
        nonlocal keep_running
        if event.key == 'q':
            keep_running = False

    print("Move the board in steps\n");
    
    while keep_running:
        # To get the interrupt status of step counter.
        int_status = sensor.get_register(BMI323_REG_INT_STATUS_INT1, 2)
        
        # To check the interrupt status of step counter.
        if (int_status[0] & BMI323_SC_REGISTER.INT_STATUS_STEP_COUNTER):
            print("Step counter interrupt is generated\n")

        # Get step counter output.
        try:
            reg_data = sensor.get_register(BMI323_REG_FEATURE_IO2, 4)
        except RuntimeError:
            continue
        
        step_count = reg_data[0]
        step_count |= reg_data[1] << 16

        # Print the step counter output.
        print(f"No of steps counted  = {step_count}")
        time.sleep(0.5)

    device.close()

if __name__ == "__main__":
    main()

