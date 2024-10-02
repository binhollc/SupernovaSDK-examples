# Demo of Pulsar I2C API

This folder contains a demonstration project to test the Pulsar host adapter I2C Protocol API. The different commands are tested showing the capabilities of the feature. For a more illustrative experience, this commands are tested using a FRAM memory [MB85RC56V](https://cdn-learn.adafruit.com/assets/assets/000/043/904/original/MB85RC256V-DS501-00017-3v0-E.pdf?1500009796) connected to the I2C Qwiic connector of the Pulsar.

## Prerequisites

- Python 3.10
- Pulsar host adapter with Qwiic connector and running `firmware version >= 3.1.0`
- Adafruit I2C Non-Volatile FRAM Breakout - 256Kbit / 32KByte

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the [I2C-Protocol-Pulsar-API.ipynb](I2C-Protocol-Pulsar-API.ipynb) notebook.