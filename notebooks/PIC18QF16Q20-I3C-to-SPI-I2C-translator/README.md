# Demo Supernova with PIC18F16Q20 board

This folder contains a demonstration project for interfacing with the PIC18F16Q20 board using the Supernova host adapter connected to the I3C High Voltage bus. The objective of this project is to utilize the [PIC18QF16Q20 as a protocol translator](https://mplab-discover.microchip.com/com.microchip.mcu8.mplabx.project.pic18f16q20-i3c-multi-protocol-translator-mplab-mcc), issuing custom I3C commands to execute the following transactions:

- I2C write

<img src="assets/i2c_write.png" alt="connection" width="80%">

- I2C read

![I2C_read](assets/i2c_read.png)

- SPI write

![SPI_write](assets/spi_write.png)

- SPI read

![SPI_read](assets/spi_read.png)

- SPI write followed by read

<img src="assets/spi_write_read.png" alt="connection" width="70%">

![Sensor_Data_Visualization](assets/stmicroelectronics_lsm6dsv_accel_gyro_plot.png)

## Prerequisites

- Python 3.10
- Supernova host adapter
- Microchip PIC18F16Q20 Curisosity Nano board plugged on the Binho PIC18F16Q20 Curisosity Nano baseboard.
- Binho PIC18F16Q20 Curisosity Nano baseboard connected to the Supernova I3C HV Port through the I3C2-1.2V connector.
- External I2C F-RAM connected to the I2C bus from the Binho PIC18QF16Q20 Curisoity Nano baseboard throught the I2C-I3C1 connector.

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the PIC18QF16Q20-I3C-to-SPI-I2C-translator notebook.
