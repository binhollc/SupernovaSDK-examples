# Demo Supernova with PIC18F16Q20 board

This folder contains a demonstration project for interfacing with the PIC18F16Q20 board using the Supernova host adapter connected to the I3C High Voltage bus. The objective of this project is to demonstrate the MTCP over I3C protocol. The demo receives multiple packets, decodes them, and assembles them into a message. And then it loops back immediately, the same message is broken down into packets and then transmitted back.


## Prerequisites

- Python >= 3.8
- binhosupernova SDK == v4.1.1
- Supernova host adapter running `firmware version >= 4.1.2`
- Microchip PIC18F16Q20 Curiosity Nano board loaded with the custom image found in the _"PIC18F16Q20 firmware image"_ folder.
- Microchip PIC18F16Q20 Curiosity Nano board plugged on the Binho PIC18F16Q20 Curiosity Nano baseboard.
- Binho PIC18F16Q20 Curiosity Nano baseboard connected to the Supernova I3C HV Port through the I3C1 connector.
- FTDI connected to the host PC and the PIC18F16Q20 UART pins.
- Serial monitor configured as 8N1 with 9600 baud rate.

## Installation

1. **Install Dependencies:**

   Use the provided `requirements.txt` to install the necessary Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow the instructions on the PIC18F16Q20-MCTP-over-I3C notebook.
