# Demo of Supernova I3C Controller API

This folder contains three different notebooks to show how to use the Supernova SDK API to set and control the Supernova device as an I3C Controller:

- [I3C-Protocol-Supernova-API.ipynb](I3C-Protocol-Supernova-API.ipynb) shows a general use case of the Supernova SDK API to initialize the I3C bus in different ways and generate I3C Private transfers, CCCs and I2C over I3C transfers.
- [I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb](I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb) shows how the Supernova SDK handles the In-Band Interrupt notification based on the TDK ICM42605 sensor.
- [I3C-Protocol-Supernova-DAA.ipynb](I3C-Protocol-Supernova-DAA.ipynb) shows different ways the Supernova can initialize the bus. This includes the dynamic address assignment and Target Device Table update.

## Prerequisites

- Python 3.10
- Supernova host adapter running `firmware version >= 2.5.0`
- To run [I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb](I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb), an ICM42605 or ICM42688 sensor is required since the notebook modifies target-specific registers to configure the In-Band Interrupt feature.
- The [I3C-Protocol-Supernova-API](I3C-Protocol-Supernova-API.ipynb) notebook shows how to set up the I3C bus using one ST LSM6DSV IMU, one Bosch BMI323 IMU and the Sparkfun EEPROM brekout board or Adafruit I2C FRAM. But it shows general I3C transfers, so it can be modified to use other targets very quickly.
- The [I3C-Protocol-Supernova-DAA.ipynb](I3C-Protocol-Supernova-DAA.ipynb) notebook shows the different methods to assign dynamic addresses to the I3C targets on the bus. The notebook is created based on a BMM350 Bosch target connected to the Supernova via the I3C HV bus. Other I3C targets may be used, but their static address and DAA allowed methods should be checked beforehand to properly test the device and understand the outcome of the evaluation.

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the [I3C-Protocol-Supernova-API.ipynb](I3C-Protocol-Supernova-API.ipynb), [I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb](I3C-Protocol-Supernova-API-ICM42605-In-Band-Interrupts.ipynb) and [I3C-Protocol-Supernova-DAA.ipynb](I3C-Protocol-Supernova-DAA.ipynb) notebooks in each case.