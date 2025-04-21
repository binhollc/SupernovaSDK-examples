# Demo of Pulsar I2C API

This folder contains a demonstration project to test the Pulsar host adapter I2C Protocol API. The different commands are tested showing the capabilities of the feature. For a more illustrative experience, the commands are tested using a FRAM memory [MB85RC56V](https://cdn-learn.adafruit.com/assets/assets/000/043/904/original/MB85RC256V-DS501-00017-3v0-E.pdf?1500009796). Although the Pulsar host adapter supports two I2C buses, this Jupyter Notebook demonstrates only the usage I2C Bus A by connecting the memory module to the I2C Qwiic connector. However, the user must use the same API method and replace the value `I2cBus.I2C_BUS_A` with the value `I2cBus.I2C_BUS_B` in the parameter `busId` to interact with the I2C Bus B. The I2C Bus B is accessible from the Breakout Board I2C SDA and SCL pins.

## Prerequisites

- Python >= 3.8
- binhopulsar SDK == v1.1.0
- Pulsar host adapter with Qwiic connector and running `firmware version >= 4.1.2`
- Adafruit I2C Non-Volatile FRAM Breakout - 256Kbit / 32KByte

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the [I2C-Protocol-Pulsar-API.ipynb](I2C-Protocol-Pulsar-API.ipynb) notebook.