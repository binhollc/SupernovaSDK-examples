"""
I2C FRAM Example with Binho Pulsar (Blocking API)
====================================================

This script demonstrates how to use the Binho Pulsar with the blocking API,
generated via the Binho Pulsar SDK and the additional blocking layer presented 
in the AN0001 document, to interface with an Adafruit I2C FRAM Breakout board.

Hardware Setup
--------------
- Binho Pulsar
- Adafruit I2C FRAM Breakout Board (I2C NVM memory)
- 3.3 V interface voltage
- I2C frequency: 1 MHz (configurable)
- I2C bus pull-ups: 2200 Ω (Configurable)

Workflow
--------
1. Connects to the first available Binho Pulsar device and initializes I2C:
   - Configures bus voltage to 3.3 V
   - Initializes I2C controller with 1 MHz clock
   - Enables 2200 Ω pull-up resistors

2. Performs an I2C bus scan:
   - Detects 7-bit and 10-bit addresses of connected devices
   - Selects the first detected 7-bit static address

3. Executes repeated write/read validation:
   - For 10 iterations:
     - Generates random-length data (1 to 1024 bytes)
     - Writes data to FRAM at address 0x0000
     - Reads back the same number of bytes from the same address
     - Validates that written and read data match

4. Closes the device connection.

Purpose
-------
This example showcases:
- How to open and configure the Binho Pulsar with the blocking API
- How to scan the I2C bus for available devices
- How to perform register-based read/write operations to an I2C FRAM memory
- How to validate data integrity across write/read cycles

References
----------
- Binho Pulsar SDK & AN0001 (Blocking Layer)
- Adafruit I2C FRAM Breakout Datasheet
- I2C Protocol Specification (UM10204, NXP)
"""

import random
from blockingpulsar import *

# Connect to the first available Pulsar device and get device info
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
result = device.i2cControllerInit(frequency=1000000, busId=I2cBus.I2C_BUS_A, pullUpResistorsValue=I2cPullUpResistorsValue.I2C_PULLUP_2_2kOhm)
print("I2C Controller Init result: ", result)

result = device.i2cControllerScanBus(busId=I2cBus.I2C_BUS_A)
print(f"I2C Scan result: "
      f"7-bit static address: {result["detected_7_bit_addresses"]} "
      f"10-bit static address: {result["detected_10_bit_addresses"]}"
      )

# Write/Read back-to-back 10 times to the first discovered device.

static_address = result["detected_7_bit_addresses"][0] #Get the first 7-bit detected address
register_address = [0,0]
        
for i in range(10):
    length = random.randint(1,1024)
    data = random.choices(range(0,256), k=length)

    print(f"\r\nIteration {i}")

    result = device.i2cControllerWrite(targetAddress=static_address, busId=I2cBus.I2C_BUS_A, registerAddress=[0x00, 0x00], data=data)
    print(f"I2C Write to 0x{static_address:02X} result: ", result)

    result = device.i2cControllerRead(targetAddress=static_address, busId=I2cBus.I2C_BUS_A, registerAddress=[0x00, 0x00], requestDataLength=len(data))
    print(f"I2C Read from 0x{static_address:02X} result: ", result)

    # Validate read data
    if result["payload"] == data:
        print("I2C Read data matches written data!")
    else:
        print("I2C Read data does NOT match written data!")

# Close the device
device.close()