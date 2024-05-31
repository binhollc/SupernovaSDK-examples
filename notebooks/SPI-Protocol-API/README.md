# Demo of Supernova SPI API

This folder contains a demonstration project to test the Supernova host adapter SPI Protocol API. In first instance, the different commands are tested showing the capabilities of the feature. For a more illustrative experience, there is a demo of the Supernova interfacing with a FRAM memory MB85RS64V connected to the SPI signals of the breakout board. The objective of this project is to utilize the [FRAM SPI Breakout](https://cdn-shop.adafruit.com/datasheets/MB85RS64V-DS501-00015-4v0-E.pdf) to write and read via SPI.

## Prerequisites

- Python 3.10
- Supernova host adapter with breakout board connected and running `firmware version >= 2.0.0`
- Adafruit SPI Non-Volatile FRAM Breakout - 64Kbit / 8KByte 

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the SPI-Protocol-Supernova-API notebook.