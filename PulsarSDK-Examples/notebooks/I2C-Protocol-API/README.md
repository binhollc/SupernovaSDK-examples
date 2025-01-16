# Demo of Pulsar I2C API

This folder contains a demonstration project to test the Pulsar host adapter I2C Protocol API. The different commands are tested showing the capabilities of the feature. For a more illustrative experience, the commands are tested using a FRAM memory [MB85RC56V](https://cdn-learn.adafruit.com/assets/assets/000/043/904/original/MB85RC256V-DS501-00017-3v0-E.pdf?1500009796). As the Pulsar host adapter supports two I2C buses, this Jupyter Notebook demonstrates their usage by connecting the memory module to the I2C Qwiic connector to interact with I2C Bus A and then to the Breakout Board I2C pins to interact with I2C Bus B.

## Prerequisites

- Python >= 3.8
- BinhoPulsar SDK == v1.0.0
- Pulsar host adapter with Qwiic connector and running `firmware version >= 4.0.0`
- Adafruit I2C Non-Volatile FRAM Breakout - 256Kbit / 32KByte

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the [I2C-Protocol-Pulsar-API.ipynb](I2C-Protocol-Pulsar-API.ipynb) notebook.